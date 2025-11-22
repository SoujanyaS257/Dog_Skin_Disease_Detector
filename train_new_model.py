import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetV2S
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import os

# --- CONFIGURATION ---
# The script looks here. Since you merged all datasets here, it trains on everything.
DATASET_PATH = "dataset/train"  
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 25  # Increased slightly since you have more data now

print(f"TensorFlow Version: {tf.__version__}")

# --- 1. Load Data ---
print("Loading combined dataset...")
if not os.path.exists(DATASET_PATH):
    print(f"❌ ERROR: Directory '{DATASET_PATH}' not found.")
    print("Please ensure your folder structure is: dataset/train/[disease_folders]")
    exit()

# Training Split (80%)
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical' # Required for multi-class
)

# Validation Split (20%)
val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

# Save the class names so the App knows them later
class_names = train_ds.class_names
print(f"✅ Classes found: {class_names}")
NUM_CLASSES = len(class_names)

# --- 2. Data Augmentation ---
# Helps the model generalize by creating "variations" of your images
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
    layers.RandomContrast(0.2),
    layers.RandomBrightness(0.2),
])

# --- 3. Build the Model (Transfer Learning) ---
# Using EfficientNetV2S (Small & Fast) - Excellent for skin diseases
base_model = EfficientNetV2S(
    include_top=False,
    weights="imagenet", 
    input_shape=(224, 224, 3)
)

base_model.trainable = False # Freeze base layers initially

inputs = tf.keras.Input(shape=(224, 224, 3))
x = data_augmentation(inputs)
x = base_model(x, training=False) 
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x) # Reduce overfitting
outputs = layers.Dense(NUM_CLASSES, activation='softmax')(x)

model = models.Model(inputs, outputs)

# --- 4. Compile ---
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# --- 5. Train Phase 1 (Base Frozen) ---
print("\n🚀 Starting Phase 1 Training (Base Frozen)...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=8
)

# --- 6. Fine-Tuning Phase 2 (Unfreeze Top Layers) ---
print("\n🚀 Starting Fine-Tuning (Phase 2)...")
base_model.trainable = True

# Freeze all layers except the last 40 (Opened up more layers since you have more data)
for layer in base_model.layers[:-40]:
    layer.trainable = False

# Recompile with low learning rate for delicate adjustments
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), 
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3)
]

history_fine = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=callbacks
)

# --- 7. Save the Result ---
os.makedirs("model", exist_ok=True)
save_path = "model/efficientnetv2s_finetuned.keras"
model.save(save_path)
print(f"\n✅ Model saved successfully to {save_path}")

# Save class names to text file
with open("model/classes.txt", "w") as f:
    f.write("\n".join(class_names))
print("✅ Class names saved to model/classes.txt")