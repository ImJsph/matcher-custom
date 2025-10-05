FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Install system deps quickly
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git curl && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

# Install CPU-only PyTorch first (prevents CUDA wheels)
RUN pip install --extra-index-url https://download.pytorch.org/whl/cpu torch==2.2.0

# Then install Python requirements (pinned in requirements.txt)
RUN pip install -r requirements.txt

# Note: we do NOT run SentenceTransformer import at build time to avoid import-version issues.
# At runtime the app will load the model. If you want to pre-warm the model in the image,
# re-add a pre-warm step *after* confirming the installed package versions are compatible:
# RUN python - <<'PY'\nfrom sentence_transformers import SentenceTransformer\nSentenceTransformer("all-MiniLM-L6-v2").save("/app/cached_model")\nPY

ENV PORT 8000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "180"]
