"""
TC24 — UI sanity: deployed frontend has three tab panels and openTab().

Checks deployment/frontend/index.html (About / Members / Predict).
Note: repo-root templates/index.html monolith has only About + Predict — TC24 targets Vercel UI.

Run from repo root:
  python testing\\verify_tc24_static.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "deployment" / "frontend" / "index.html"


def main():
    html = PATH.read_text(encoding="utf-8")

    print("TC24 - Tab UI (static check on", PATH.name + ")")

    checks = [
        ('onclick="openTab(event, \'about\')"', "About tab"),
        ('onclick="openTab(event, \'members\')"', "Members tab"),
        ('onclick="openTab(event, \'predict\')"', "Predict tab"),
        ('id="about"', "about panel"),
        ('id="members"', "members panel"),
        ('id="predict"', "predict panel"),
        ("function openTab(", "openTab()"),
    ]

    ok = True
    for needle, label in checks:
        hit = needle in html
        print(f"  {'OK' if hit else 'MISSING'} {label}")
        ok = ok and hit

    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
