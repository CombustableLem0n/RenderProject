import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os

dataset_path = r"C:\Users\legol\OneDrive\Desktop\RenderProject\renders"
dataset_root = r"C:\Users\legol\OneDrive\Desktop\RenderProject"
train_dir = os.path.join(dataset_root, "train")
val_dir = os.path.join(dataset_root, "val")

train_gen = ImageDataGenerator(rescale=1./255, rotation_range=30, zoom_range=0.2,
                                horizontal_flip=True)
val_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    train_dir, target_size=(224, 224), batch_size=9, class_mode='categorical'
)
val_data = val_gen.flow_from_directory(
    val_dir, target_size=(224, 224), batch_size=9, class_mode='categorical'
)

base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(train_data.num_classes, activation='softmax')  # One output for each LEGO part
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_data, validation_data=val_data, epochs=10)

test_gen = ImageDataGenerator(rescale=1./255)
test_data = test_gen.flow_from_directory(
    train_dir, target_size=(224, 224), batch_size=9, class_mode='categorical'
)

test_loss, test_acc = model.evaluate(test_data)
print(f"Test Accuracy: {test_acc:.2f}")

import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

image_path = r"C:\Users\legol\OneDrive\Desktop\RenderProject\test_brick2.png"
img = load_img(image_path, target_size=(224, 224))
img_array = img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

predictions = model.predict(img_array)
class_idx = np.argmax(predictions[0])
class_label = list(train_data.class_indices.keys())[class_idx]

print(f"Predicted LEGO part: {class_label}")