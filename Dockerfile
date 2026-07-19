# Use Python 3.10 to satisfy modern package dependencies
FROM python:3.10-slim

# Prevent Python from writing .pyc files and force stdout logging
ENV PYTHONTONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system build tools required by heavy Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly download the spaCy English model 
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY . .

# Run Gunicorn using shell form
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 4 --timeout 120 app:app"
