import tensorflow as tf
import numpy as np
import cv2
from .model import model, preprocess_image, IMG_SIZE

def get_grad_cam(img_bytes, last_conv_layer_name="top_conv"):
    """
    Generates a Grad-CAM heatmap for a given image.
    """
    if model is None:
        return None

    img_array = preprocess_image(img_bytes)

    try:
        grad_model = tf.keras.models.Model(
            [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
        )
    except ValueError:
        print(f"Layer '{last_conv_layer_name}' not found. Checking model summary for correct layer names.")
        # Heuristic fallback for EfficientNetV2S.
        # This name is typical for the final convolutional block.
        last_conv_layer_name = model.layers[-5].name
        print(f"Trying fallback layer name: '{last_conv_layer_name}'")
        try:
            grad_model = tf.keras.models.Model(
                [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
            )
        except Exception as e:
            print(f"Could not create Grad-CAM model: {e}")
            return None

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        # This is the new, crucial line that fixes the error.
        tape.watch(last_conv_layer_output)
        pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)

    # Handle cases where gradient is None
    if grads is None:
        print("Gradient could not be computed. Returning None.")
        return None

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    heatmap = heatmap.numpy()

    # Superimpose heatmap on original image
    from PIL import Image
    import io

    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    img = img.resize(IMG_SIZE)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    superimposed_img = heatmap * 0.4 + img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)
    superimposed_img = cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB)

    return superimposed_img