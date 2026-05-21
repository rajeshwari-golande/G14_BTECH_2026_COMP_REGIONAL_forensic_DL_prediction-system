"""
TC18 — Performance: 20 sequential POST /api/predict (same PNG) after warm-up.

Measures per-request latency; optionally enforces DOCUMENTED_SLO_MS_PER_REQUEST.

Environment:
  TC18_API_URL   Base URL, no trailing slash. Default Railway URL from frontend.
  DOCUMENTED_SLO_MS_PER_REQUEST   Max latency per predict after warm-up (ms). Default 120000.

Requires: pip install requests pillow

Run from repo root:
  python testing/verify_tc18.py
"""
from __future__ import annotations

import io
import os
import statistics
import sys
import time
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
    os.environ.get("TC18_API_URL")
    or "https://celebrated-compassion-production-b17c.up.railway.app"
).rstrip("/")

# Conservative default for ML on shared CPU inference (tune via env).
DEFAULT_SLO_MS = float(os.environ.get("DOCUMENTED_SLO_MS_PER_REQUEST", "120000"))

WARMUP_COUNT = max(1, int(os.environ.get("TC18_WARMUP", "1")))
N_RUNS = 20


def make_png_bytes() -> bytes:
    img = Image.new("RGB", (128, 128), color=(180, 180, 185))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def post_predict(session: requests.Session, base: str, png: bytes) -> tuple[bool, float, int]:
    url = base + "/api/predict"
    t0 = time.perf_counter()
    r = session.post(
        url,
        files={"file": ("finger.png", png, "image/png")},
        timeout=900,
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    ok = r.status_code == 200
    try:
        data = r.json()
        ok = ok and data.get("success") is True
    except Exception:
        ok = False
    return ok, elapsed_ms, r.status_code


def main():
    png = make_png_bytes()
    base = DEFAULT_API

    slo = DEFAULT_SLO_MS
    print(f"TC18 - 20 sequential predicts (warm-up x{WARMUP_COUNT})")
    print(f"API base: {base}")
    print(f"SLO ceiling (DOCUMENTED_SLO_MS_PER_REQUEST): {slo:g} ms / request")

    session = requests.Session()

    print("Warm-up...")
    for i in range(WARMUP_COUNT):
        ok, ms, status = post_predict(session, base, png)
        print(f"  warm-up [{i + 1}]: HTTP {status} ok={ok} {ms:.0f} ms")
        if not ok:
            print("FAIL warm-up returned non-success")
            sys.exit(1)

    latencies: list[float] = []
    for i in range(N_RUNS):
        ok, ms, status = post_predict(session, base, png)
        latencies.append(ms)
        if not ok:
            print(f"FAIL run {i + 1}: HTTP {status}")
            sys.exit(1)
        if ms > slo:
            print(f"FAIL run {i + 1}: {ms:.0f} ms exceeds SLO {slo:g} ms")
            sys.exit(1)
        print(f"  [{i + 1:02d}/{N_RUNS}] {ms:.0f} ms  OK")

    print("Summary (ms): min {:.0f}, max {:.0f}, mean {:.0f}".format(
        min(latencies), max(latencies), statistics.mean(latencies),
    ))

    print("PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
