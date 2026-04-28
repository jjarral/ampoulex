# Ampoulex ERP - Developer Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Getting Started](#getting-started)
4. [Project Structure](#project-structure)
5. [Development Guidelines](#development-guidelines)
6. [API Reference](#api-reference)
7. [Database Schema](#database-schema)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

## Introduction

Ampoulex is a comprehensive Enterprise Resource Planning (ERP) system designed for ampoule manufacturing businesses. It provides end-to-end business management capabilities including:

- Product Management
- Order Processing
- Customer Relationship Management
- Supplier Management
- Inventory Control
- Production Tracking
- Quality Control
- Accounting & Financials
- HR & Payroll
- Tax Compliance

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.11+, Flask 3.0.0 |
| Database | PostgreSQL 13+ |
| ORM | SQLAlchemy 3.1.1 |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |
| UI Framework | AdminLTE 3.2 |
| Charts | Chart.js 4.5 |
| Real-time | Flask-SocketIO 5.3.6 |
| Testing | pytest |

## Architecture Overview

### Application Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Browser                        │
│              (HTML/CSS/JavaScript)                       │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/WebSocket
┌────────────────────▼────────────────────────────────────┐
│                  Flask Application                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Blueprints│  │ Services │  │  Models  │              │
│  └──────────┘  └──────────┘  └──────────┘              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │   Auth   │  │Products  │  │ Customers│              │
│  └──────────┘  └──────────┘  └──────────┘              │
└────────────────────┬────────────────────────────────────┘
                     │ SQLAlchemy ORM
┌────────────────────▼────────────────────────────────────┐
│                   PostgreSQL Database                    │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
ampoulex/
├── app/                          # Main application package
│   ├── __init__.py              # App factory & extensions
│   ├── models.py                # Database models
│   ├── routes.py                # Legacy routes (being refactored)
│   ├── forms.py                 # WTForms forms
│   ├── utils.py                 # Utility functions
│   ├── email_helper.py          # Email functionality
│   ├── blueprints/              # Modular blueprints
│   │   ├── auth/               # Authentication
│   │   ├── products/           # Product management
│   │   ├── orders/             # Order management
│   │   └── ...
│   ├── services/               # Business logic layer
│   │   ├── product_service.py
│   │   └── ...
│   └── utils/
│       └── tax_calculator.py
├── templates/                   # Jinja2 templates
├── static/                      # Static assets
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── app.js
├── tests/                       # Test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── migrations/                  # Database migrations
├── docs/                        # Documentation
├── scripts/                     # Deployment scripts
├── backups/                     # Database backups
├── .env.example                # Environment template
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose
├── requirements.txt            # Python dependencies
└── run.py                      # Development server
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 13 or higher
- Git
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jjarral/ampoulex.git
   cd ampoulex
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Create database**
   ```bash
   createdb ampoulex_db
   ```

6. **Run migrations**
   ```bash
   flask db upgrade
   ```

7. **Start development server**
   ```bash
   python run.py
   ```

Visit `http://localhost:5000`

### Default Credentials

- Username: `admin`
- Password: `admin123`

## Development Guidelines

### Code Style

- Follow PEP 8 style guide for Python code
- Use type hints where possible
- Write docstrings for all public functions and classes
- Keep functions small and focused (Single Responsibility Principle)

### Naming Conventions

- **Variables**: snake_case (`user_name`, `total_amount`)
- **Functions**: snake_case (`get_user_by_id`, `calculate_total`)
- **Classes**: PascalCase (`UserService`, `ProductController`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`)

### Git Workflow

1. Create feature branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make commits with clear messages
   ```bash
   git commit -m "feat: add user authentication"
   ```

3. Push and create pull request
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

```
type: subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

## API Reference

### Authentication Endpoints

#### POST /auth/login
Login user

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

#### GET /auth/logout
Logout current user

### Product Endpoints

#### GET /products
List all products

**Query Parameters:**
- `page` (int): Page number
- `per_page` (int): Items per page
- `search` (string): Search term
- `type` (string): Product type filter

#### POST /products/new
Create new product

#### PUT /products/<id>/edit
Update product

#### DELETE /products/<id>/delete
Delete product (soft delete)

## Database Schema

### Core Tables

- `user` - User accounts
- `product` - Product catalog
- `customer` - Customer information
- `order` - Sales orders
- `order_item` - Order line items
- `supplier` - Supplier information
- `purchase_order` - Purchase orders
- `warehouse` - Warehouse locations
- `warehouse_stock` - Stock by warehouse
- `production_batch` - Production batches
- `raw_material` - Raw materials
- `bom_item` - Bill of materials
- `qc_parameter` - QC parameters
- `account` - Chart of accounts
- `journal_entry` - Journal entries
- `employee` - Employee records
- `attendance` - Attendance records

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/unit/test_product_service.py

# Run specific test
pytest tests/unit/test_product_service.py::TestProductService::test_create_product
```

### Writing Tests

```python
import pytest
from unittest.mock import patch, MagicMock

from app.services.product_service import ProductService

class TestProductService:
    def test_create_product(self):
        with patch('app.services.product_service.db') as mock_db:
            # Arrange
            mock_session = MagicMock()
            mock_db.session = mock_session
            
            product_data = {
                'name': 'Test Product',
                'sku': 'TEST-001'
            }
            
            # Act
            result = ProductService.create_product(product_data)
            
            # Assert
            assert result.name == 'Test Product'
            mock_session.add.assert_called_once()
```

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t ampoulex .

# Run container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/ampoulex \
  -e SECRET_KEY=your-secret-key \
  ampoulex
```

### Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT-ID/ampoulex

# Deploy
gcloud run deploy ampoulex \
  --image gcr.io/PROJECT-ID/ampoulex \
  --platform managed \
  --region us-central1
```

## Troubleshooting

### Common Issues

#### Database Connection Error

**Problem:** Cannot connect to database

**Solution:**
1. Check DATABASE_URL in .env
2. Verify PostgreSQL is running
3. Check network connectivity
4. Ensure SSL mode is configured for cloud databases

```bash
# Test connection
psql $DATABASE_URL
```

#### Import Errors

**Problem:** ModuleNotFoundError

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

#### Port Already in Use

**Problem:** Address already in use

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
export PORT=5001
python run.py
```

### Logs

Check application logs for errors:
```bash
# Development
tail -f logs/ampoulex.log

# Docker
docker logs <container-id>
```

### Support

For additional help:
- Open an issue on GitHub
- Check existing documentation
- Review error logs

---

**Last Updated:** 2025-04-28
**Version:** 1.0.0
