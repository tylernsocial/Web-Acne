## goal of script: 
# load model
# load class names
# preprocess image
# return prediction

import json ## loads class_names.json
import numpy as np ## converts images into an array the model can understand
import tensorflow as tf ## loads final_model.keras and runs predictions
from PIL import Image ## used for opening and resizing uploaded images 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent # find the folder where predict.py is located.
MODEL_PATH = BASE_DIR / "model" / "mobilenetv2_acne_classifier.keras"
CLASS_NAMES_PATH = BASE_DIR / "model" / "class_names.json"

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r") as f:
    class_names = json.load(f)

def preprocess_image(image_file):
    '''
    prepares an uploaded image so it matches the format expected by the model
    '''
    img = Image.open(image_file)

    rgb_img = img.convert('RGB')

    resized_img = rgb_img.img.resize((224, 224))

    img_array = np.array(resized_img)

    img_array = img_array / 255.0 ## normalize pixel values from 0-255 to 0-1 since cnn works better on smaller values

    img_array = np.expand_dims(img_array, axis=0)

    return img_array