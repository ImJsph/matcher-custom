FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential git curl && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

# Install CPU PyTorch first (from official PyTorch CPU index)
RUN pip install --extra-index-url https://download.pytorch.org/whl/cpu torch==2.2.0

# Then install the rest
RUN pip install -r requirements.txt

# Optional: pre-warm the sentence-transformers model (this will increase image size & build time)
RUN python - <<'PY'
from sentence_transformers import SentenceTransformer
SentenceTransformer("all-MiniLM-L6-v2").save("/app/cached_model")
PY

# Use gunicorn to serve
ENV PORT 8000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "1"]
