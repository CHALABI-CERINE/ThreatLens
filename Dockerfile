# Use an official, secure slim image
FROM python:3.11-slim

WORKDIR /app

# Install system deps needed for building some packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application source
COPY src /app/src

# Create directory for persistent data (SQLite file)
RUN mkdir -p /app/data
VOLUME ["/app/data"]

EXPOSE 8501

ENV THREATLENS_DATABASE="sqlite:///data/threatlens.db"
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

# Run via gunicorn (install gunicorn in requirements.txt or in venv)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8501", "src.app:app", "--timeout", "120"]
