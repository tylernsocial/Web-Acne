## goal of predict.py:
# load model
# load class names
# preprocess image
# return prediction

import json ## loads class_names.json
import numpy as np ## converts images into an array the model can understand
import tensorflow as tf ## loads final_model.keras and runs predictions
from PIL import Image, UnidentifiedImageError ## used for opening and resizing uploaded images
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent # find the folder where predict.py is located.
MODEL_PATH = BASE_DIR / "model" / "mobilenetv2_acne_classifier.keras"
CLASS_NAMES_PATH = BASE_DIR / "model" / "class_names.json"

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r") as f:
    class_names = json.load(f)


def resize_with_padding(image, target_size=(224, 224), fill_color=(0, 0, 0)):
    """
    Resize an image while preserving its aspect ratio, then pad it to the target size.
    This matches the preprocessing used during model training.
    """
    image = image.convert("RGB")
    image.thumbnail(target_size)

    new_image = Image.new("RGB", target_size, fill_color)

    x_offset = (target_size[0] - image.width) // 2
    y_offset = (target_size[1] - image.height) // 2

    new_image.paste(image, (x_offset, y_offset))

    return new_image


def preprocess_image(image_file):
    """
    Prepares an uploaded image so it matches the format expected by the model.
    """
    try:
        img = Image.open(image_file)

        processed_img = resize_with_padding(img, target_size=(224, 224), fill_color=(0, 0, 0))

        img_array = np.array(processed_img).astype("float32")
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        return img_array

    except UnidentifiedImageError:
        raise ValueError("Uploaded file is not a valid image.")


def predict_acne_class(image_file):
    """
    Runs the model on an image and returns the predicted class and confidence.
    """

    processed_img = preprocess_image(image_file)
    predictions = model.predict(processed_img)

    predicted_index = int(np.argmax(predictions[0]))
    confidence = float(np.max(predictions[0]))
    predicted_class = class_names[predicted_index]

    return {
        "prediction": predicted_class,
        "confidence": round(confidence * 100, 2)
    }
