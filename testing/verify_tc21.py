"""
TC21 — Boundary: large JPEG POST /api/predict, then health check.

Builds an in-memory JPEG (no repo file). Verifies 200 + success within timeout,
then GET /api/health = 200 + {"status":"ok"}.

Environment:
  TC21_API_URL              Base URL (no trailing slash); default Railway URL.
  TC21_JPEG_MAX_SIDE        Max width/height in pixels (default 2400). Increase for stress.
  TC21_JPEG_QUALITY         1-95 (default 90).
  TC21_TIMEOUT_SEC          Per-request timeout for predict (default 600).
  TC21_HEALTH_TIMEOUT_SEC   Health request timeout (default 60).

Requires: pip install requests pillow

Run from repo root:
  python testing\verify_tc21.py
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
    os.environ.get("TC21_API_URL")
    or os.environ.get("TC20_API_URL")
    or os.environ.get("TC18_API_URL")
    or "https://celebrated-compassion-production-b17c.up.railway.app"
).rstrip("/")

MAX_SIDE = max(512, int(os.environ.get("TC21_JPEG_MAX_SIDE", "2400")))
JPEG_Q = max(1, min(95, int(os.environ.get("TC21_JPEG_QUALITY", "90"))))
PRED_TIMEOUT = float(os.environ.get("TC21_TIMEOUT_SEC", "600"))
HEALTH_TIMEOUT = float(os.environ.get("TC21_HEALTH_TIMEOUT_SEC", "60"))


def large_jpeg_bytes() -> tuple[bytes, int, int]:
    """Square RGB noise-ish pattern so JPEG compresses moderately."""
    img = Image.new("RGB", (MAX_SIDE, MAX_SIDE), color=(210, 200, 190))
    # Light variation so JPEG is not trivially tiny
    pixels = img.load()
    step = max(16, MAX_SIDE // 128)
    for y in range(0, MAX_SIDE, step):
        for x in range(0, MAX_SIDE, step):
            v = ((x ^ y) * 37) % 40
            for dy in range(min(step, MAX_SIDE - y)):
                for dx in range(min(step, MAX_SIDE - x)):
                    if x + dx < MAX_SIDE and y + dy < MAX_SIDE:
                        pixels[x + dx, y + dy] = (180 + v, 160 + v, 140 + v)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_Q, optimize=True)
    return buf.getvalue(), MAX_SIDE, MAX_SIDE


def main():
    jpeg, w, h = large_jpeg_bytes()
    base = DEFAULT_API

    mb = len(jpeg) / (1024 * 1024)
    print(f"TC21 - Large JPEG boundary")
    print(f"API base: {base}")
    print(f"JPEG size: {w}x{h}px, ~{mb:.2f} MiB compressed, quality={JPEG_Q}")

    predict_url = base + "/api/predict"
    try:
        r = requests.post(
            predict_url,
            files={"file": ("boundary_large.jpg", jpeg, "image/jpeg")},
            timeout=PRED_TIMEOUT,
        )
    except requests.Timeout:
        print(f"FAIL: predict exceeded timeout ({PRED_TIMEOUT}s)")
        sys.exit(1)

    print("POST /api/predict HTTP", r.status_code)
    ok = r.status_code == 200
    try:
        data = r.json()
    except Exception:
        print("FAIL: predict response not JSON")
        sys.exit(1)

    if not ok or not data.get("success"):
        print("FAIL:", data)
        sys.exit(1)

    need = ("blood_group", "gender", "blood_confidence", "gender_confidence", "blood_scores")
    missing = [k for k in need if k not in data]
    if missing:
        print("FAIL: missing JSON keys:", missing)
        sys.exit(1)

    hc = requests.get(base + "/api/health", timeout=HEALTH_TIMEOUT)
    ok_h = hc.status_code == 200 and (hc.json() or {}).get("status") == "ok"
    print("GET /api/health HTTP", hc.status_code, "ok=", ok_h)
    if not ok_h:
        print("FAIL health after large predict")
        sys.exit(1)

    print("PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
