"""
TC06 harness: PATCH blood predictor to simulate failure without touching production API.
Run from repo root: python testing/verify_tc06.py
"""
import io
import sys
from pathlib import Path
from unittest.mock import patch

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "deployment" / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from PIL import Image  # noqa: E402

from app import app  # noqa: E402


def fake_blood_failure(_model, _image_array):
    return {
        "blood_group": None,
        "confidence": 0.0,
        "all_scores": {},
        "success": False,
        "error": "Forced blood failure for TC06",
    }


def main():
    img = Image.new("RGB", (64, 64), color="gray")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    client = app.test_client()
    with patch("app.predict_blood_group", side_effect=fake_blood_failure):
        resp = client.post(
            "/api/predict",
            data={"file": (buf, "test.png")},
            content_type="multipart/form-data",
        )

    payload = resp.get_json(silent=True)
    print("Status:", resp.status_code)
    print("JSON:", payload)

    ok = resp.status_code == 500 and payload and payload.get("success") is False
    ok = ok and "Blood group error:" in (payload.get("error") or "")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
