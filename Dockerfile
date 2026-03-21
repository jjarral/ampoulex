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

# Create necessary directories for static files
RUN mkdir -p static/reports static/barcodes static/qrcodes static/logos

# Expose port (Cloud Run expects 8080)
EXPOSE 8080

# Run with gunicorn (production WSGI server)
CMD exec gunicorn --bind :8080 --workers 4 --threads 8 --timeout 0 app:create_app()