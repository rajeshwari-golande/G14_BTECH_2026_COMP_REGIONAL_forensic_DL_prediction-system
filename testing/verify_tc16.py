"""
TC16 — Integration: GET / returns 200 and forensic UI HTML.

Validates the same template the monolith serves (templates/index.html) without
importing full app.py (avoids TensorFlow / gdown on import).

For the exact line in app.py: @app.route('/') -> render_template('index.html')

Run from repo root:
  python testing/verify_tc16.py
"""
import os
import sys
from pathlib import Path

from flask import Flask, render_template

REPO_ROOT = Path(__file__).resolve().parents[1]
os.chdir(REPO_ROOT)

app = Flask(__name__, template_folder=str(REPO_ROOT / "templates"))


@app.route("/")
def index():
    return render_template("index.html")


def main():
    client = app.test_client()
    resp = client.get("/")
    html = resp.get_data(as_text=True)

    print("TC16 - Monolith home GET / (same templates/ as app.py)")
    print("status:", resp.status_code)
    marker = "Forensic Fingerprint Analysis"
    found = marker in html
    print(marker + ":", "found in HTML" if found else "MISSING")

    ok = resp.status_code == 200
    ok = ok and resp.content_type.startswith("text/html")
    ok = ok and "<!DOCTYPE html>" in html
    ok = ok and found

    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
