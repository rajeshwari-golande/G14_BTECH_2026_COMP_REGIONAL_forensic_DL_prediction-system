"""
TC14 — Unit: Hugging Face download disabled via env.

With DISABLE_HF_MODEL_DOWNLOAD=1, _huggingface_repo_id() must return None.

Run from repo root:
  python testing/verify_tc14.py

PowerShell (manual):
  $env:DISABLE_HF_MODEL_DOWNLOAD="1"
  cd deployment\\backend
  python -c "import os; os.environ['DISABLE_HF_MODEL_DOWNLOAD']='1'; from ml.model_loader import _huggingface_repo_id; print(_huggingface_repo_id())"
"""
import os
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "deployment" / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Must be set before importing modules that might cache — set early anyway.
os.environ["DISABLE_HF_MODEL_DOWNLOAD"] = "1"

from ml.model_loader import _huggingface_repo_id  # noqa: E402


def main():
    rid = _huggingface_repo_id()
    print("TC14 - HF download off")
    print("_huggingface_repo_id():", repr(rid))
    ok = rid is None
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
