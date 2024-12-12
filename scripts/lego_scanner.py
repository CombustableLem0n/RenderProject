import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os
import shutil
import random

# Directory paths
dataset_path = r"C:\Users\legol\OneDrive\Desktop\RenderProject\test_data"  # Folder containing subfolders for each object
output_path = r"C:\Users\legol\OneDrive\Desktop\RenderProject\train_val_split"  # Folder to store the split train/val data

# Create train and val directories
train_dir = os.path.join(output_path, "train")
val_dir = os.path.join(output_path, "val")

# Function to clear the contents of a directory
def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Remove subdirectories
        else:
            os.remove(file_path)  # Remove files

# Clear the contents of train and val directories if they already exist
if os.path.exists(train_dir):
    clear_directory(train_dir)
else:
    os.makedirs(train_dir)

if os.path.exists(val_dir):
    clear_directory(val_dir)
else:
    os.makedirs(val_dir)

# Create subdirectories for each class in train and val
object_folders = [folder for folder in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, folder))]
for folder in object_folders:
    os.makedirs(os.path.join(train_dir, folder), exist_ok=True)
    os.makedirs(os.path.join(val_dir, folder), exist_ok=True)

# Split the images into train and validation sets
for folder in object_folders:
    folder_path = os.path.join(dataset_path, folder)
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Shuffle the images to randomize the split
    random.shuffle(image_files)
    
    # Define split ratio (80% for training, 20% for validation)
    train_size = int(0.8 * len(image_files))
    val_size = len(image_files) - train_size
    
    train_images = image_files[:train_size]
    val_images = image_files[train_size:]
    
    # Move images to their respective directories
    for image in train_images:
        shutil.copy(os.path.join(folder_path, image), os.path.join(train_dir, folder, image))
    
    for image in val_images:
        shutil.copy(os.path.join(folder_path, image), os.path.join(val_dir, folder, image))

print(f"Data has been split into training and validation sets.")

# Create ImageDataGenerators for training and validation
train_gen = ImageDataGenerator(rescale=1./255, rotation_range=30, zoom_range=0.2,
                                horizontal_flip=True)
val_gen = ImageDataGenerator(rescale=1./255)

# Flow data from directories, automatically infers class labels from subfolder names
train_data = train_gen.flow_from_directory(
    train_dir, 
    target_size=(224, 224), 
    batch_size=9, 
    class_mode='categorical'
)

val_data = val_gen.flow_from_directory(
    val_dir, 
    target_size=(224, 224), 
    batch_size=9, 
    class_mode='categorical'
)

# Load MobileNetV2 as the base model
base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base_model.trainable = False

# Create the model
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(train_data.num_classes, activation='softmax')  # One output for each LEGO part
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(train_data, validation_data=val_data, epochs=6)

# Evaluate the model on the validation data
test_loss, test_acc = model.evaluate(val_data)
print(f"Validation Accuracy: {test_acc:.2f}")

# Make predictions on a new image
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Path to the image you want to classify
image_path = r"C:\Users\legol\OneDrive\Desktop\RenderProject\test_images\test_mask5.png"
img = load_img(image_path, target_size=(224, 224))
img_array = img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Make predictions
predictions = model.predict(img_array)
class_idx = np.argmax(predictions[0])
class_label = list(train_data.class_indices.keys())[class_idx]

print(f"Predicted LEGO part: {class_label}")
