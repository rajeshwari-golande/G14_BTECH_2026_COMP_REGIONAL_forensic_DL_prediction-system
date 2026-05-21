"""
TC19 — Load: 10 parallel POST /api/predict, then GET /api/health.

Reports success ratio for concurrent predicts; health must be 200 with {"status":"ok"}.

Environment:
  TC19_API_URL                   Base URL (no trailing slash); default same as TC18 Railway URL.
  TC19_MIN_SUCCESS_RATIO          Min fraction of parallel predicts that must succeed (0–1). Default 1.0.

Requires: pip install requests pillow

Run from repo root:
  python testing/verify_tc19.py
"""
from __future__ import annotations

import io
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    os.environ.get("TC19_API_URL")
    or os.environ.get("TC18_API_URL")
    or "https://celebrated-compassion-production-b17c.up.railway.app"
).rstrip("/")

PARALLEL = max(1, int(os.environ.get("TC19_PARALLEL", "10")))
MIN_RATIO = float(os.environ.get("TC19_MIN_SUCCESS_RATIO", "1.0"))


def png_bytes() -> bytes:
    img = Image.new("RGB", (128, 128), color=(180, 180, 185))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def predict_once(base: str, png: bytes) -> bool:
    """One POST; OK if HTTP 200 and JSON success."""
    url = base + "/api/predict"
    try:
        r = requests.post(
            url,
            files={"file": ("finger.png", png, "image/png")},
            timeout=900,
        )
        if r.status_code != 200:
            return False
        data = r.json()
        return data.get("success") is True
    except Exception:
        return False


def health_ok(base: str) -> tuple[bool, int]:
    """GET /api/health."""
    url = base + "/api/health"
    try:
        r = requests.get(url, timeout=60)
        if r.status_code != 200:
            return False, r.status_code
        data = r.json()
        return data.get("status") == "ok", r.status_code
    except Exception:
        return False, -1


def main():
    png = png_bytes()
    base = DEFAULT_API

    print("TC19 - Load burst + health")
    print(f"API base: {base}")
    print(f"Parallel predicts: {PARALLEL}")
    print(f"Min success ratio: {MIN_RATIO:g}")

    ok_flags: list[bool] = []
    with ThreadPoolExecutor(max_workers=PARALLEL) as pool:
        futures = [pool.submit(predict_once, base, png) for _ in range(PARALLEL)]
        for i, fut in enumerate(as_completed(futures), start=1):
            ok = fut.result()
            ok_flags.append(ok)
            print(f"  parallel job done ({i}/{PARALLEL}): {'OK' if ok else 'FAIL'}")

    n_ok = sum(ok_flags)
    ratio = n_ok / PARALLEL
    print(f"Success ratio: {n_ok}/{PARALLEL} = {ratio:.2%} (document for report)")

    if ratio + 1e-9 < MIN_RATIO:
        print(f"FAIL: below minimum {MIN_RATIO:g}")
        sys.exit(1)

    h_ok, h_code = health_ok(base)
    print(f"GET /api/health: HTTP {h_code}, status ok={h_ok}")
    if not h_ok:
        print("FAIL: health check after burst")
        sys.exit(1)

    print("PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
