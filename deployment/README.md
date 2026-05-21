# Split Deployment (Render + Railway)

This folder gives you a separate deployment setup so your existing `app.py` flow remains untouched.

- `backend/` -> deploy to Railway (hosts ML models + prediction API)
- `frontend/` -> deploy to Render Static Site (UI only)

## 1) Deploy backend to Railway

### A. Create Railway service from `deployment/backend`
- Root directory: `deployment/backend`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300`

### B. Configure model files
Because models are heavy, keep them outside the frontend host.

Use one of these:
- **Option 1 (recommended):** Railway volume mounted at `/data/models`
  - Upload `blood_group.h5` and `gender_model.keras` into that directory.
- **Option 2:** set direct file paths with env vars:
  - `BLOOD_GROUP_MODEL_PATH`
  - `GENDER_MODEL_PATH`

Optional env var:
- `MODEL_DIR=/data/models`
- `CORS_ORIGINS=https://<your-render-site>.onrender.com`

### C. Verify backend
- `GET /api/health` should return `{ "status": "ok" }`
- Note your backend URL:
  - Example: `https://fingerprint-api-production.up.railway.app`

## 2) Deploy frontend to Render (Static Site)

### A. Create static site from `deployment/frontend`
- Publish directory: `deployment/frontend`
- Build command: *(leave empty for plain static files)*

### B. Connect frontend to backend
- Open the deployed page.
- In **Railway Backend URL** field, paste your Railway URL.
- This value is stored in browser local storage, so you only set it once per browser.

## 3) Local test of split setup

From repo root:

1. Start backend:
   - `cd deployment/backend`
   - `python app.py`
2. Open frontend file:
   - `deployment/frontend/index.html` (or serve it via any static server)
3. Set backend URL in UI to:
   - `http://127.0.0.1:5000`

## Notes

- This split architecture is valid for free-tier constraints.
- If Railway memory becomes tight with TensorFlow, use a larger Railway plan or optimize models (quantization/format conversion).
