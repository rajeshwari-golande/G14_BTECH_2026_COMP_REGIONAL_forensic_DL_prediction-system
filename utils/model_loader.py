"""
Model loading utilities for fingerprint analysis models
"""

import os
import pickle
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import TensorFlow
import tensorflow as tf

# Configure paths
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"

# Model paths
BLOOD_GROUP_MODEL_PATH = os.environ.get(
    "BLOOD_GROUP_MODEL_PATH",
    str(MODELS_DIR / "blood_group.h5")
)
GENDER_MODEL_PATH = os.environ.get(
    "GENDER_MODEL_PATH", 
    str(MODELS_DIR / "gender_model.keras")
)

# Global variables to cache loaded models
_blood_group_model = None
_gender_model = None


def load_blood_group_model():
    """Load the blood group prediction model"""
    global _blood_group_model
    
    if _blood_group_model is not None:
        return _blood_group_model
    
    try:
        if BLOOD_GROUP_MODEL_PATH.endswith(('.h5', '.keras')):
            try:
                _blood_group_model = tf.keras.models.load_model(BLOOD_GROUP_MODEL_PATH)
            except Exception as e:
                # Fallback: load without compile
                print(f"⚠️ Trying compile=False...")
                _blood_group_model = tf.keras.models.load_model(BLOOD_GROUP_MODEL_PATH, compile=False)
                _blood_group_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        elif BLOOD_GROUP_MODEL_PATH.endswith('.pkl'):
            with open(BLOOD_GROUP_MODEL_PATH, 'rb') as f:
                _blood_group_model = pickle.load(f)
        elif BLOOD_GROUP_MODEL_PATH.endswith('.joblib'):
            _blood_group_model = joblib.load(BLOOD_GROUP_MODEL_PATH)
        else:
            raise ValueError(f"Unsupported format: {BLOOD_GROUP_MODEL_PATH}")
        
        print(f"✓ Blood group model loaded")
        return _blood_group_model
    
    except Exception as e:
        raise Exception(f"Error loading blood group model: {str(e)}")


def load_gender_model():
    """Load the gender classification model"""
    global _gender_model
    
    if _gender_model is not None:
        return _gender_model
    
    try:
        if GENDER_MODEL_PATH.endswith(('.h5', '.keras')):
            try:
                _gender_model = tf.keras.models.load_model(GENDER_MODEL_PATH)
            except Exception as e:
                # Fallback: load without compile
                print(f"⚠️ Trying compile=False...")
                _gender_model = tf.keras.models.load_model(GENDER_MODEL_PATH, compile=False)
                _gender_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        elif GENDER_MODEL_PATH.endswith('.pkl'):
            with open(GENDER_MODEL_PATH, 'rb') as f:
                _gender_model = pickle.load(f)
        elif GENDER_MODEL_PATH.endswith('.joblib'):
            _gender_model = joblib.load(GENDER_MODEL_PATH)
        else:
            raise ValueError(f"Unsupported format: {GENDER_MODEL_PATH}")
        
        print(f"✓ Gender model loaded")
        return _gender_model
    
    except Exception as e:
        raise Exception(f"Error loading gender model: {str(e)}")


def set_model_paths(blood_group_path, gender_path):
    """Update model paths at runtime"""
    global BLOOD_GROUP_MODEL_PATH, GENDER_MODEL_PATH
    global _blood_group_model, _gender_model
    
    BLOOD_GROUP_MODEL_PATH = blood_group_path
    GENDER_MODEL_PATH = gender_path
    
    # Clear cached models
    _blood_group_model = None
    _gender_model = None
    
    print(f"Model paths updated successfully")
