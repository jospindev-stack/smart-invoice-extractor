FROM python:3.11-slim

# Prevents Python from writing .pyc files and buffers stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir \
    fastapi==0.115.5 \
    "uvicorn[standard]==0.32.0" \
    python-multipart==0.0.12 \
    pdfplumber==0.11.4 \
    groq==0.12.0 \
    python-dotenv==1.0.1 \
    pydantic==2.10.3 \
    pydantic-settings==2.6.1

COPY backend/ ./backend/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
