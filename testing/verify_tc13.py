"""
TC13 — Unit: Gender mock inference.

Mock model returns [[0.2, 0.8]] (two-class); expect:
  success: true; gender Male; finite confidence

Run from repo root:
  python testing/verify_tc13.py
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "deployment" / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

import numpy as np  # noqa: E402

from ml.predictor import predict_gender  # noqa: E402


class MockGenderModelTwoClass:
    """TC13 spec: predict() -> (1, 2) row [0.2, 0.8] -> argmax 1 -> Male."""

    def predict(self, image_array, verbose=0):
        return np.array([[0.2, 0.8]], dtype=np.float32)


def main():
    model = MockGenderModelTwoClass()
    arr = np.zeros((224, 224, 1), dtype=np.float32)

    r = predict_gender(model, arr)
    print("TC13 - Gender mock inference")
    print("result:", r)

    ok = r.get("success") is True
    ok = ok and r.get("gender") == "Male"
    conf = r.get("confidence")
    ok = ok and isinstance(conf, (int, float)) and np.isfinite(conf)

    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
