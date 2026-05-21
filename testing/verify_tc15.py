"""
TC15 — Integration: ensure_remote_models() when weights already exist in MODEL_DIR.

Placeholder files satisfy "local weights present"; download helpers must not run.

Run from repo root:
  python testing/verify_tc15.py
"""
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "deployment" / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Isolate model dir and block HF for this run
os.environ["DISABLE_HF_MODEL_DOWNLOAD"] = "1"
for key in (
    "BLOOD_GROUP_MODEL_URL",
    "GENDER_MODEL_URL",
    "BLOOD_GROUP_MODEL_PATH",
    "GENDER_MODEL_PATH",
):
    os.environ.pop(key, None)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        os.environ["MODEL_DIR"] = str(tmp_path)

        # Names checked by ensure_remote_models() (either file skips HTTP/HF for that spec)
        (tmp_path / "blood_group.h5").write_bytes(b"placeholder")
        (tmp_path / "gender_model.keras").write_bytes(b"placeholder")

        from ml.model_loader import ensure_remote_models  # noqa: E402

        def no_http_download(*_a, **_kw):
            raise AssertionError("_download_to must not run when local weights exist")

        def no_hf_download(*_a, **_kw):
            raise AssertionError("_download_from_huggingface must not run when local weights exist")

        print("TC15 - Local weights present (idempotent ensure_remote_models)")

        with patch("ml.model_loader._download_to", side_effect=no_http_download):
            with patch("ml.model_loader._download_from_huggingface", side_effect=no_hf_download):
                ensure_remote_models()
                ensure_remote_models()

        print("PASS (no download path executed)")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL:", exc)
        sys.exit(1)
