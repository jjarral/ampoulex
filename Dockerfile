# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy ALL application code (including templates/ and static/)
COPY . .

RUN mkdir -p static/reports static/barcodes static/qrcodes static/logos

# Expose port (Cloud Run expects 8080)
EXPOSE 8080

# ✅ CORRECT: Use $PORT environment variable from Cloud Run
CMD exec gunicorn --bind :$PORT --workers 4 --threads 8 --timeout 300 --access-logfile - --error-logfile - app:create_app