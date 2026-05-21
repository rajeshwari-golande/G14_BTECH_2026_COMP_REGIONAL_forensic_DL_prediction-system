# Pins Python + OS so pip gets correct wheels (avoids Railpack/Python 3.13 + numpy/tf conflicts).
FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Used by scipy/sklearn/tf binary wheels on slim images
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

# Railway injects PORT; workers=1 keeps one TF model set in memory per process.
CMD ["/bin/sh", "-c", "exec gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --timeout 300 --workers 1"]
