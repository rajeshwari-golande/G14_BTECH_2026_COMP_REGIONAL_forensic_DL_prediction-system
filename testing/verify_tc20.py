"""
TC20 — Boundary: POST /api/predict with minimal 1x1 PNG.

Expected per test matrix (Pass): HTTP 200, success: true, full prediction payload.

Environment:
  TC20_API_URL   Base URL, no slash. Defaults to Railway URL shared with TC18.

Requires: pip install requests pillow

Run from repo root:
  python testing\verify_tc20.py
"""
from __future__ import annotations

import io
import os
import sys

try:
    import requests
except ImportError:
    print("ERROR: pip install requests")
    sys.exit(2)

try:
    from PIL import Image
except ImportError:
    print("ERROR: pip install pillow")
    sys.exit(2)

DEFAULT_API = (
    os.environ.get("TC20_API_URL")
    or os.environ.get("TC18_API_URL")
    or "https://celebrated-compassion-production-b17c.up.railway.app"
).rstrip("/")


def one_by_one_png() -> bytes:
    img = Image.new("RGB", (1, 1), color=(42, 42, 42))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def main():
    png = one_by_one_png()
    url = DEFAULT_API + "/api/predict"

    print("TC20 - Boundary 1x1 PNG")
    print(f"POST {url}")

    r = requests.post(
        url,
        files={"file": ("tiny.png", png, "image/png")},
        timeout=900,
    )
    print("HTTP", r.status_code)

    ok = r.status_code == 200
    try:
        data = r.json()
    except Exception:
        print("FAIL: not JSON")
        sys.exit(1)

    if not ok or not data.get("success"):
        print("FAIL:", data)
        sys.exit(1)

    need = ("blood_group", "gender", "blood_confidence", "gender_confidence", "blood_scores")
    missing = [k for k in need if k not in data]
    if missing:
        print("FAIL: missing keys", missing)
        sys.exit(1)

    print("blood_group:", data.get("blood_group"))
    print("gender:", data.get("gender"))
    print("PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
