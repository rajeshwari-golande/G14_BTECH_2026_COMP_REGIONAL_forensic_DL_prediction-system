"""
TC23 — Security: CORS allowlist in production (no open * for real deployments).

Where implemented:
  deployment/backend/app.py — CORS_ORIGINS env (default "*" for local dev only).

Live check (default):
  OPTIONS /api/predict with Origin = expected Vercel URL; response must echo that
  exact origin in Access-Control-Allow-Origin (not "*").

Environment:
  TC23_API_BASE       e.g. https://celebrated-compassion-production-b17c.up.railway.app (no path)
  TC23_EXPECTED_ORIGIN  e.g. https://forensic-prediction.vercel.app

Requires: pip install requests

Run from repo root:
  python testing\\verify_tc23.py
"""
from __future__ import annotations

import os
import sys

try:
    import requests
except ImportError:
    print("ERROR: pip install requests")
    sys.exit(2)

BASE = (
    os.environ.get("TC23_API_BASE")
    or os.environ.get("TC20_API_URL")
    or "https://celebrated-compassion-production-b17c.up.railway.app"
).rstrip("/")

ORIGIN = (
    os.environ.get("TC23_EXPECTED_ORIGIN")
    or "https://forensic-prediction.vercel.app"
).rstrip("/")


def main():
    url = BASE + "/api/predict"

    print("TC23 - CORS allowlist (production behaviour)")
    print("OPTIONS", url)
    print("Origin header:", ORIGIN)

    r = requests.options(
        url,
        headers={
            "Origin": ORIGIN,
            "Access-Control-Request-Method": "POST",
        },
        timeout=60,
    )

    acao = (r.headers.get("Access-Control-Allow-Origin") or "").strip()
    print("HTTP", r.status_code)
    print("Access-Control-Allow-Origin:", repr(acao))

    ok = r.status_code in (200, 204)
    ok = ok and acao == ORIGIN
    ok = ok and acao != "*"

    print("PASS" if ok else "FAIL (expect exact origin echo, not *)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
