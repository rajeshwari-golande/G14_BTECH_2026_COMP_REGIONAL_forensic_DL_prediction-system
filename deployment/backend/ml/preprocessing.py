import cv2
import numpy as np
from PIL import Image


def preprocess_fingerprint(image: Image.Image, model_type: str = "gender", target_size: tuple = None) -> np.ndarray:
    if model_type == "blood_group":
        target_size = target_size or (150, 150)
        output_channels = 3
    else:
        target_size = target_size or (224, 224)
        output_channels = 1

    img_array = np.array(image)
    if len(img_array.shape) == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    img_resized = cv2.resize(img_array, target_size, interpolation=cv2.INTER_AREA)
    img_normalized = img_resized.astype("float32") / 255.0
    img_normalized = cv2.equalizeHist((img_normalized * 255).astype(np.uint8)).astype(np.float32) / 255.0

    if output_channels == 3:
        return np.stack([img_normalized, img_normalized, img_normalized], axis=-1)
    return np.expand_dims(img_normalized, axis=-1)
