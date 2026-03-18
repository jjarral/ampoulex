FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create folders for static files if they don't exist
RUN mkdir -p static/reports static/barcodes static/qrcodes static/logos instance

# Expose port
EXPOSE 8080

# Run with Gunicorn (Production Server)
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 wsgi:app