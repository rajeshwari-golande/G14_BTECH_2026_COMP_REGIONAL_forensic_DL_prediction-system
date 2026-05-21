"""
TC10 — Unit: Blood preprocessing contract.

PIL RGB → preprocess_fingerprint(..., "blood_group")
Expected: shape (150, 150, 3), float32, values in [0, 1]

Run from repo root:
  python testing/verify_tc10.py
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "deployment" / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from ml.preprocessing import preprocess_fingerprint  # noqa: E402


def main():
    img = Image.new("RGB", (64, 64), color=128)
    arr = preprocess_fingerprint(img, model_type="blood_group")

    ok_shape = arr.shape == (150, 150, 3)
    ok_dtype = arr.dtype == np.float32
    lo, hi = float(arr.min()), float(arr.max())
    ok_range = 0.0 <= lo <= hi <= 1.0

    print("TC10 - Blood preprocessing")
    print("shape:", arr.shape, "(expected (150, 150, 3))")
    print("dtype:", arr.dtype, "(expected float32)")
    print("min, max:", lo, hi, "(expected in [0, 1])")
    print("PASS" if (ok_shape and ok_dtype and ok_range) else "FAIL")

    sys.exit(0 if (ok_shape and ok_dtype and ok_range) else 1)


if __name__ == "__main__":
    main()
