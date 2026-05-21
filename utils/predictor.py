"""
Prediction functions for fingerprint analysis models
"""

import numpy as np
from typing import Dict, Any


# Blood group classes
BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']


def predict_blood_group(model, image_array: np.ndarray) -> Dict[str, Any]:
    """
    Predict blood group from fingerprint image
    
    Args:
        model: Loaded blood group model
        image_array: Preprocessed image array (150x150x3)
    
    Returns:
        Dictionary with prediction results
    """
    try:
        # Ensure image has batch dimension
        if len(image_array.shape) == 3:
            image_array = np.expand_dims(image_array, axis=0)
        
        print(f"DEBUG: Blood group input shape: {image_array.shape}")
        print(f"DEBUG: Blood group input min/max: {image_array.min()}/{image_array.max()}")
        
        # Get predictions
        predictions = model.predict(image_array, verbose=0)
        
        print(f"DEBUG: Raw predictions shape: {predictions.shape}")
        print(f"DEBUG: Raw predictions: {predictions[0]}")
        print(f"DEBUG: Raw predictions min/max: {predictions.min()}/{predictions.max()}")
        
        # Apply softmax if values look like logits (large range)
        if np.max(np.abs(predictions)) > 50:
            print("DEBUG: Applying softmax...")
            predictions = np.exp(predictions) / np.sum(np.exp(predictions), axis=1, keepdims=True)
        
        # Handle different output shapes
        if predictions.shape[1] == len(BLOOD_GROUPS):
            # Multiple classes (classification)
            confidence = np.max(predictions[0])
            predicted_class = np.argmax(predictions[0])
            predicted_blood_group = BLOOD_GROUPS[predicted_class]
            
            # Get all scores
            all_scores = {BLOOD_GROUPS[i]: float(predictions[0][i]) 
                         for i in range(len(BLOOD_GROUPS))}
        else:
            # Different output size, map to blood groups
            confidence = np.max(predictions[0])
            predicted_class = np.argmax(predictions[0])
            predicted_blood_group = BLOOD_GROUPS[min(predicted_class, len(BLOOD_GROUPS)-1)]
            
            all_scores = {BLOOD_GROUPS[i]: float(predictions[0][i]) 
                         for i in range(min(len(predictions[0]), len(BLOOD_GROUPS)))}
        
        print(f"DEBUG: Final confidence: {confidence}")
        
        return {
            "blood_group": predicted_blood_group,
            "confidence": float(confidence),
            "all_scores": all_scores,
            "success": True
        }
    
    except Exception as e:
        print(f"ERROR in predict_blood_group: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "blood_group": None,
            "confidence": 0.0,
            "all_scores": {},
            "success": False,
            "error": str(e)
        }


def predict_gender(model, image_array: np.ndarray) -> Dict[str, Any]:
    """
    Predict gender from fingerprint image
    
    Args:
        model: Loaded gender classification model
        image_array: Preprocessed image array (224x224x1)
    
    Returns:
        Dictionary with prediction results
    """
    try:
        # Ensure image has batch dimension
        if len(image_array.shape) == 3:
            image_array = np.expand_dims(image_array, axis=0)
        
        print(f"DEBUG (gender): Input shape: {image_array.shape}")
        print(f"DEBUG (gender): Input min/max: {image_array.min()}/{image_array.max()}")
        
        # Get prediction
        prediction = model.predict(image_array, verbose=0)
        
        print(f"DEBUG (gender): Raw predictions shape: {prediction.shape}")
        print(f"DEBUG (gender): Raw predictions: {prediction[0]}")
        print(f"DEBUG (gender): Raw predictions min/max: {prediction.min()}/{prediction.max()}")
        
        # Apply softmax if values look like logits
        if np.max(np.abs(prediction)) > 50:
            print("DEBUG (gender): Applying softmax...")
            prediction = np.exp(prediction) / np.sum(np.exp(prediction), axis=1, keepdims=True)
        
        # Handle different output shapes
        if prediction.shape[1] == 1:
            # Binary classification: single output (sigmoid)
            confidence = float(prediction[0][0])
            predicted_gender = "Female" if confidence < 0.5 else "Male"
            # Adjust confidence to be distance from 0.5
            confidence = abs(confidence - 0.5) * 2
        else:
            # Binary classification: two outputs (softmax)
            confidence = float(np.max(prediction[0]))
            predicted_class = np.argmax(prediction[0])
            predicted_gender = "Female" if predicted_class == 0 else "Male"
        
        print(f"DEBUG (gender): Final confidence: {confidence}")
        
        return {
            "gender": predicted_gender,
            "confidence": confidence,
            "success": True
        }
    
    except Exception as e:
        print(f"ERROR in predict_gender: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "gender": None,
            "confidence": 0.0,
            "success": False,
            "error": str(e)
        }
