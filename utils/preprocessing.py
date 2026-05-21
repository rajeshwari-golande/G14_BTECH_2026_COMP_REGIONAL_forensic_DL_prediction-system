"""
Image preprocessing utilities for fingerprint images
"""

import cv2
import numpy as np
from PIL import Image


def preprocess_fingerprint(image: Image.Image, model_type: str = "gender", target_size: tuple = None) -> np.ndarray:
    """
    Preprocess fingerprint image for model prediction
    
    Args:
        image: PIL Image object
        model_type: "blood_group" or "gender" - determines preprocessing
        target_size: Override target size
    
    Returns:
        Preprocessed numpy array with correct shape for the model
    """
    # Set target size and channels based on model type
    if model_type == "blood_group":
        target_size = target_size or (150, 150)
        output_channels = 3  # RGB
    else:  # gender
        target_size = target_size or (224, 224)
        output_channels = 1  # Grayscale
    
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    
    # Convert to grayscale first
    if len(img_array.shape) == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Resize to target size
    img_resized = cv2.resize(img_array, target_size, interpolation=cv2.INTER_AREA)
    
    # Normalize pixel values to 0-1 range
    img_normalized = img_resized.astype('float32') / 255.0
    
    # Apply histogram equalization for better contrast
    img_normalized = cv2.equalizeHist((img_normalized * 255).astype(np.uint8)).astype(np.float32) / 255.0
    
    # Format output based on model type
    if output_channels == 3:
        # Blood group: Convert grayscale to RGB by repeating channels
        img_output = np.stack([img_normalized, img_normalized, img_normalized], axis=-1)
    else:
        # Gender: Keep as grayscale with single channel
        img_output = np.expand_dims(img_normalized, axis=-1)
    
    print(f"DEBUG preprocessing ({model_type}): Output shape = {img_output.shape}, min/max = {img_output.min()}/{img_output.max()}")
    
    return img_output


def enhance_fingerprint(image: np.ndarray) -> np.ndarray:
    """
    Enhance fingerprint features using image processing techniques
    
    Args:
        image: Fingerprint image as numpy array
    
    Returns:
        Enhanced image array
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Apply morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    enhanced = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    enhanced = cv2.morphologyEx(enhanced, cv2.MORPH_OPEN, kernel)
    
    # Apply median filter to remove noise
    enhanced = cv2.medianBlur(enhanced, 5)
    
    return enhanced


def normalize_fingerprint(image: np.ndarray) -> np.ndarray:
    """
    Normalize fingerprint image using standard normalization
    
    Args:
        image: Fingerprint image as numpy array
    
    Returns:
        Normalized image array
    """
    if len(image.shape) == 3 and image.shape[-1] == 3:
        # RGB normalization
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        return (image - mean) / std
    else:
        # Grayscale normalization
        mean = 0.5
        std = 0.5
        return (image - mean) / std
