"""
TC22 — Security / config: Frontend PRODUCTION_BACKEND uses HTTPS production URL.

Reads deployment/frontend/index.html (no runtime browser).

Run from repo root:
  python testing\\verify_tc22.py

Optional:
  TC22_FRONTEND_HTML  Path to index.html override.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path


def extract_backend(html: str) -> str | None:
    m = re.search(
        r'const\s+PRODUCTION_BACKEND\s*=\s*"([^"]*)"',
        html,
        re.MULTILINE,
    )
    return m.group(1).strip() if m else None


def main():
    root = Path(__file__).resolve().parents[1]
    path = Path(
        os.environ.get("TC22_FRONTEND_HTML")
        or (root / "deployment" / "frontend" / "index.html")
    )
    if not path.exists():
        print("FAIL: frontend index not found:", path)
        sys.exit(1)

    html = path.read_text(encoding="utf-8")
    url = extract_backend(html)

    print("TC22 - PRODUCTION_BACKEND (frontend)")
    print("file:", path)
    print("value:", repr(url) if url is not None else None)

    ok = url is not None and len(url) > 0
    ok = ok and url.startswith("https://")
    ok = ok and not url.startswith("http://")
    ok = ok and "your-railway-service" not in url.lower()
    ok = ok and "localhost" not in url.lower() and "127.0.0.1" not in url.lower()

    print("PASS" if ok else "FAIL (expect https:// production URL, no placeholder)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
