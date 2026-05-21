import os
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image

from ml.model_loader import ensure_remote_models, load_blood_group_model, load_gender_model
from ml.predictor import predict_blood_group, predict_gender
from ml.preprocessing import preprocess_fingerprint

app = Flask(__name__)

# You can lock this down later with CORS_ORIGINS env var.
cors_origins = os.environ.get("CORS_ORIGINS", "*")
CORS(app, resources={r"/api/*": {"origins": cors_origins}})

blood_model = None
gender_model = None


def load_models_once():
    global blood_model, gender_model
    ensure_remote_models()
    if blood_model is None:
        blood_model = load_blood_group_model()
    if gender_model is None:
        gender_model = load_gender_model()
    return blood_model, gender_model


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/predict")
def predict():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected"}), 400

    try:
        image = Image.open(file.stream)

        blood_model_local, gender_model_local = load_models_once()

        preprocessed_blood = preprocess_fingerprint(image, model_type="blood_group")
        preprocessed_gender = preprocess_fingerprint(image, model_type="gender")

        blood_result = predict_blood_group(blood_model_local, preprocessed_blood)
        gender_result = predict_gender(gender_model_local, preprocessed_gender)

        if not blood_result["success"] or not gender_result["success"]:
            error_parts = []
            if not blood_result["success"]:
                error_parts.append(f"Blood group error: {blood_result.get('error', 'Unknown')}")
            if not gender_result["success"]:
                error_parts.append(f"Gender error: {gender_result.get('error', 'Unknown')}")
            return jsonify({"success": False, "error": ". ".join(error_parts)}), 500

        return jsonify(
            {
                "success": True,
                "blood_group": blood_result["blood_group"],
                "blood_confidence": float(blood_result["confidence"]),
                "blood_scores": blood_result["all_scores"],
                "gender": gender_result["gender"],
                "gender_confidence": float(gender_result["confidence"]),
            }
        )
    except Exception as exc:
        return jsonify({"success": False, "error": f"Error processing image: {exc}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
