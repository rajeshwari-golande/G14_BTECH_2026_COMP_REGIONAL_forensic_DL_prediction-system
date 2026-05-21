"""
TC17 — Integration: monolith POST /predict with valid file returns 200 HTML.

Patches predictors so TensorFlow/Keras model load is skipped; still exercises real
routes in app.py + templates/index.html.

Requires repo-root dependencies (pip install -r requirements.txt).

Run from repo root:
  python testing/verify_tc17.py
"""
import io
import os
import sys
import types
from pathlib import Path
from unittest.mock import patch

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
os.chdir(REPO_ROOT)
sys.path.insert(0, str(REPO_ROOT))


def _ensure_gdown():
    """app.py imports gdown — stub if missing (no downloads in this harness)."""
    if "gdown" not in sys.modules:
        try:
            import gdown  # noqa: F401
        except ImportError:
            m = types.ModuleType("gdown")
            m.download = lambda *a, **kw: None
            sys.modules["gdown"] = m


def main():
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    _ensure_gdown()

    from app import app  # noqa: E402 — after cwd + path + gdown
    import app as app_mod  # noqa: E402

    tiny = Image.new("RGB", (64, 64), color=(200, 200, 200))
    buf = io.BytesIO()
    tiny.save(buf, format="PNG")
    buf.seek(0)

    fake_blood = {"blood_group": "O+", "confidence": 0.88}
    fake_gender = {"gender": "Female", "confidence": 0.77}

    app_mod.blood_model = object()
    app_mod.gender_model = object()

    client = app.test_client()
    with patch.object(app_mod, "predict_blood_group", return_value=fake_blood):
        with patch.object(app_mod, "predict_gender", return_value=fake_gender):
            resp = client.post(
                "/predict",
                data={"file": (buf, "finger.png")},
                content_type="multipart/form-data",
            )

    html = resp.get_data(as_text=True)

    print("TC17 - Monolith POST /predict")
    print("status:", resp.status_code)

    ok = resp.status_code == 200
    ok = ok and resp.content_type.startswith("text/html")
    ok = ok and "O+" in html and "Female" in html

    print("PASS" if ok else "FAIL")
    if not ok and resp.status_code != 200:
        print("(first 400 chars)", html[:400])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
