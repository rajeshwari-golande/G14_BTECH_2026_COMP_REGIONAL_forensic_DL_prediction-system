from flask import Flask, request, render_template
from PIL import Image
import os
import gdown

from utils.model_loader import (
    load_blood_group_model,
    load_gender_model,
    set_model_paths
)
from utils.predictor import predict_blood_group, predict_gender
from utils.preprocessing import preprocess_fingerprint

app = Flask(__name__)

blood_model = None
gender_model = None

# -------------------------------
# MODEL SETUP
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

blood_model_path = os.path.join(MODEL_DIR, "blood_group.h5")
gender_model_path = os.path.join(MODEL_DIR, "gender_model.keras")

# ✅ Google Drive links (YOURS)
blood_url = "https://drive.google.com/uc?id=1kQkyeNrjXa7tAu8TMcd9_tp6RMbxewiC"
gender_url = "https://drive.google.com/uc?id=1ZIzhcRIfvRis_QJZnflAgc5Xl31ncOXY"


# -------------------------------
# DOWNLOAD FUNCTION (FIXED)
# -------------------------------

def download_file(url, path):
    print(f"\nDownloading {path}...")

    # 🔥 Remove old file (important)
    if os.path.exists(path):
        os.remove(path)

    gdown.download(url, path, quiet=False)

    size = os.path.getsize(path)
    print(f"Downloaded size: {size}")

    # 🔥 Check if download is valid
    if size < 50000000:  # <50MB means broken
        print("❌ File corrupted, retrying...")
        os.remove(path)
        gdown.download(url, path, quiet=False)


def ensure_models_exist():
    # Blood model (~200MB)
    if (not os.path.exists(blood_model_path)) or os.path.getsize(blood_model_path) < 50000000:
        download_file(blood_url, blood_model_path)

    # Gender model (small)
    if (not os.path.exists(gender_model_path)) or os.path.getsize(gender_model_path) < 1000000:
        download_file(gender_url, gender_model_path)


# -------------------------------
# ROUTES
# -------------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    global blood_model, gender_model

    if 'file' not in request.files:
        return render_template('index.html', results={'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', results={'error': 'No file selected'})
    
    try:
        image = Image.open(file.stream)

        # 🔥 LOAD MODELS ONLY WHEN USER CLICKS
        if blood_model is None or gender_model is None:
            print("Downloading + Loading models...")

            ensure_models_exist()
            set_model_paths(blood_model_path, gender_model_path)

            try:
                blood_model = load_blood_group_model()
                print("✅ Blood model loaded")
            except Exception as e:
                print("❌ Blood model error:", e)
                blood_model = None

            try:
                gender_model = load_gender_model()
                print("✅ Gender model loaded")
            except Exception as e:
                print("❌ Gender model error:", e)
                gender_model = None

        if blood_model is None or gender_model is None:
            return render_template('index.html', results={
                'error': "Model loading failed. Check logs."
            })

        # 🔥 Prediction
        preprocessed_blood = preprocess_fingerprint(image, model_type="blood_group")
        preprocessed_gender = preprocess_fingerprint(image, model_type="gender")

        blood_result = predict_blood_group(blood_model, preprocessed_blood)
        gender_result = predict_gender(gender_model, preprocessed_gender)

        return render_template('index.html', results={
            'blood_group': blood_result['blood_group'],
            'blood_confidence': f"{blood_result['confidence']:.2%}",
            'gender': gender_result['gender'],
            'gender_confidence': f"{gender_result['confidence']:.2%}"
        })

    except Exception as e:
        return render_template('index.html', results={'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
