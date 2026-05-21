from typing import Any, Dict

import numpy as np

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


def predict_blood_group(model, image_array: np.ndarray) -> Dict[str, Any]:
    try:
        if len(image_array.shape) == 3:
            image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array, verbose=0)
        if np.max(np.abs(predictions)) > 50:
            predictions = np.exp(predictions) / np.sum(np.exp(predictions), axis=1, keepdims=True)

        confidence = np.max(predictions[0])
        predicted_class = np.argmax(predictions[0])
        predicted_blood_group = BLOOD_GROUPS[min(predicted_class, len(BLOOD_GROUPS) - 1)]
        all_scores = {
            BLOOD_GROUPS[i]: float(predictions[0][i]) for i in range(min(len(predictions[0]), len(BLOOD_GROUPS)))
        }

        return {
            "blood_group": predicted_blood_group,
            "confidence": float(confidence),
            "all_scores": all_scores,
            "success": True,
        }
    except Exception as exc:
        return {
            "blood_group": None,
            "confidence": 0.0,
            "all_scores": {},
            "success": False,
            "error": str(exc),
        }


def predict_gender(model, image_array: np.ndarray) -> Dict[str, Any]:
    try:
        if len(image_array.shape) == 3:
            image_array = np.expand_dims(image_array, axis=0)

        prediction = model.predict(image_array, verbose=0)
        if np.max(np.abs(prediction)) > 50:
            prediction = np.exp(prediction) / np.sum(np.exp(prediction), axis=1, keepdims=True)

        if prediction.shape[1] == 1:
            confidence = float(prediction[0][0])
            predicted_gender = "Female" if confidence < 0.5 else "Male"
            confidence = abs(confidence - 0.5) * 2
        else:
            confidence = float(np.max(prediction[0]))
            predicted_class = np.argmax(prediction[0])
            predicted_gender = "Female" if predicted_class == 0 else "Male"

        return {"gender": predicted_gender, "confidence": confidence, "success": True}
    except Exception as exc:
        return {"gender": None, "confidence": 0.0, "success": False, "error": str(exc)}
