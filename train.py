import tensorflow as tf
import os

# --- Configuration ---
DATASET_PATH = 'dataset'
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS_FEATURE_EXTRACTION = 5  # Epochs for the first phase
EPOCHS_FINE_TUNING = 10        # Epochs for the second phase
LEARNING_RATE = 0.001
# After
MODEL_SAVE_PATH = 'model/checkpoints/efficientnetv2s_model.keras'

# --- 1. Load and Prepare the Dataset ---
print("Loading and preparing dataset...")

# Create the checkpoints directory if it doesn't exist
os.makedirs('model/checkpoints', exist_ok=True)

# Load dataset from folders
train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_dataset.class_names
num_classes = len(class_names)
print(f"Found classes: {class_names}")

# Configure dataset for performance
AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)

# --- 2. Create Data Augmentation Layers ---
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal'),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomBrightness(0.2),
])

# --- 3. Build the Model ---
print("Building the EfficientNetV2-S model...")

# Load the pre-trained base model
base_model = tf.keras.applications.EfficientNetV2S(
    input_shape=(224, 224, 3),
    include_top=False,  # Do not include the final classification layer
    weights='imagenet'
)

# Freeze the base model layers
base_model.trainable = False

# Create the new model on top
inputs = tf.keras.Input(shape=(224, 224, 3))
x = data_augmentation(inputs)
x = tf.keras.applications.efficientnet_v2.preprocess_input(x)
x = base_model(x, training=False)  # Set training=False for frozen layers
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.3)(x)
outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)

model = tf.keras.Model(inputs, outputs)

# --- 4. Phase 1: Feature Extraction Training ---
print("\n--- Starting Phase 1: Feature Extraction ---")
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_dataset,
    epochs=EPOCHS_FEATURE_EXTRACTION,
    validation_data=validation_dataset
)

# --- 5. Phase 2: Fine-Tuning ---
print("\n--- Starting Phase 2: Fine-Tuning ---")
base_model.trainable = True

# Unfreeze the top layers of the model
# Let's fine-tune from the 40th layer onwards
for layer in base_model.layers[:-40]:
    layer.trainable = False

# Re-compile the model with a lower learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Continue training
history_fine = model.fit(
    train_dataset,
    epochs=EPOCHS_FEATURE_EXTRACTION + EPOCHS_FINE_TUNING,
    initial_epoch=history.epoch[-1], # Continue from where we left off
    validation_data=validation_dataset
)

# --- 6. Save the Final Model ---
print(f"\nTraining complete. Saving model to {MODEL_SAVE_PATH}")
model.save(MODEL_SAVE_PATH)
print("Model saved successfully! You can now run the Streamlit app.")