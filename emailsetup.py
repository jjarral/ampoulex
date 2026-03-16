#!/usr/bin/env python3
"""Create all production deployment files"""

import os

print("="*70)
print("🚀 CREATING PRODUCTION DEPLOYMENT FILES")
print("="*70)

# 1. wsgi.py
wsgi_content = """from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
"""

with open('wsgi.py', 'w') as f:
    f.write(wsgi_content)
print("✅ Created: wsgi.py")

# 2. Dockerfile
dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p static/reports static/barcodes static/qrcodes static/logos instance

# Expose port
EXPOSE 8080

# Run with gunicorn for production
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 wsgi:app
"""

with open('Dockerfile', 'w') as f:
    f.write(dockerfile_content)
print("✅ Created: Dockerfile")

# 3. .dockerignore
dockerignore_content = """# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Virtual environments
venv/
.venv/
env/
.env
.env.production

# Database
*.db
*.sqlite
*.sqlite3
instance/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Static files (generated)
static/reports/*
static/barcodes/*
static/qrcodes/*
static/logos/*

# Git
.git/
.gitignore

# Documentation
README.md
*.md

# Test
.pytest_cache/
.coverage
htmlcov/

# Build
dist/
build/
*.egg-info/
"""

with open('.dockerignore', 'w') as f:
    f.write(dockerignore_content)
print("✅ Created: .dockerignore")

# 4. .gitignore
gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
.env
.env.production
*.egg-info/
dist/
build/

# Database
*.db
*.sqlite
*.sqlite3
instance/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Static files (generated)
static/reports/*
static/barcodes/*
static/qrcodes/*
static/logos/*

# Test
.pytest_cache/
.coverage
htmlcov/

# Docker
.dockerignore
Dockerfile
"""

with open('.gitignore', 'w') as f:
    f.write(gitignore_content)
print("✅ Created: .gitignore")

# 5. requirements.txt (update)
requirements_content = """Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-SocketIO==5.3.6
python-dotenv==1.0.0
Werkzeug==3.0.1
email-validator==2.1.0
python-barcode==0.15.1
qrcode==7.4.2
Pillow==10.1.0
openpyxl==3.1.2
reportlab==4.0.7
gunicorn==21.2.0
psycopg2-binary==2.9.9
"""

with open('requirements.txt', 'w') as f:
    f.write(requirements_content)
print("✅ Created: requirements.txt")

print("\n" + "="*70)
print("✅ ALL PRODUCTION FILES CREATED!")
print("="*70)
print("\n🎯 NEXT STEPS:")
print("   1. Create Bitbucket repository")
print("   2. Push code: git add . && git commit -m 'Production ready' && git push")
print("   3. Set up Firebase project")
print("   4. Deploy to Cloud Run")
print("="*70)