"""
TC12 — Unit: Blood mock inference (8-class output).

Mock model returns shape (1, 8); predict_blood_group must return:
  success: true; blood_group in BLOOD_GROUPS; 8 entries in all_scores

Run from repo root:
  python testing/verify_tc12.py
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "deployment" / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

import numpy as np  # noqa: E402

from ml.predictor import BLOOD_GROUPS, predict_blood_group  # noqa: E402


class MockBloodModel8Class:
    """Keras-like .predict — 8 logits (softmax applied in code only if |x| > 50)."""

    def predict(self, image_array, verbose=0):
        # Slightly favor class index 2 so argmax is stable and not uniform tie.
        row = np.array([0.05, 0.05, 0.40, 0.25, 0.10, 0.05, 0.05, 0.05], dtype=np.float32)
        return np.array([row])


def main():
    model = MockBloodModel8Class()
    # 3D array triggers batch dim inside predict_blood_group
    arr = np.zeros((150, 150, 3), dtype=np.float32)

    r = predict_blood_group(model, arr)
    print("TC12 - Blood mock inference")
    print("result:", r)

    ok = r.get("success") is True
    ok = ok and r.get("blood_group") in BLOOD_GROUPS
    scores = r.get("all_scores") or {}
    ok = ok and len(scores) == 8
    ok = ok and set(scores.keys()) == set(BLOOD_GROUPS)

    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
