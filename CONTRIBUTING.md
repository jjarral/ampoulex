# Contributing to Ampoulex

Thank you for your interest in contributing to Ampoulex! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Accept constructive criticism
- Focus on what's best for the community

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/ampoulex.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Node.js 18+
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/your-username/ampoulex.git
cd ampoulex

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your database credentials
# DATABASE_URL=postgresql://user:pass@localhost:5432/ampoulex_db

# Create database
createdb ampoulex_db

# Run migrations
flask db upgrade

# Start development server
python run.py
```

### Docker Development

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t ampoulex .
docker run -p 8080:8080 --env-file .env ampoulex
```

## Project Structure

```
ampoulex/
├── app/                      # Main application package
│   ├── __init__.py          # App factory and extensions
│   ├── models.py            # Database models
│   ├── routes.py            # Route handlers
│   ├── forms.py             # WTForms forms
│   ├── utils.py             # Utility functions
│   ├── email_helper.py      # Email functionality
│   └── utils/               # Additional utilities
│       ├── __init__.py
│       └── tax_calculator.py
├── templates/               # Jinja2 templates
│   ├── base.html           # Base template
│   ├── dashboard.html      # Dashboard
│   ├── auth/               # Authentication templates
│   ├── products/           # Product management
│   ├── orders/             # Order management
│   ├── customers/          # Customer management
│   ├── suppliers/          # Supplier management
│   ├── accounting/         # Accounting module
│   ├── production/         # Production module
│   ├── qc/                 # Quality control
│   ├── payroll/            # HR & Payroll
│   └── ...                 # Other modules
├── static/                  # Static assets
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   ├── images/             # Images
│   └── ...                 # Generated files (barcodes, qrcodes, etc.)
├── migrations/              # Database migrations
├── tests/                   # Test suite
├── scripts/                 # Deployment scripts
├── backups/                 # Database backups
├── artifacts/               # Design artifacts and mockups
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
├── wsgi.py                 # WSGI entry point
├── run.py                  # Development server
└── README.md               # This file
```

## Coding Standards

### Python

- Follow PEP 8 style guidelines
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions focused and small (< 50 lines preferred)
- Use meaningful variable names

```python
# Good
def calculate_total_amount(items: list[dict]) -> float:
    """Calculate total amount from list of items."""
    return sum(item['price'] * item['quantity'] for item in items)

# Bad
def calc(l):
    t = 0
    for i in l:
        t += i['p'] * i['q']
    return t
```

### Templates

- Use template inheritance (extend `base.html`)
- Keep business logic out of templates
- Use macros for reusable components
- Comment complex sections

```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content_header %}
<h1><i class="fas fa-box"></i> Products</h1>
{% endblock %}

{% block content %}
<!-- Your content here -->
{% endblock %}
```

### Database Models

- Use descriptive table names
- Include timestamps (created_at, updated_at)
- Add indexes for frequently queried columns
- Use foreign keys with proper cascading

```python
class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
```

### Routes

- Use blueprints for organization
- Include proper error handling
- Validate input data
- Use decorators for authentication/authorization

```python
@main_bp.route('/products/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """Edit an existing product."""
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Validate and process form
            product.name = request.form['name']
            db.session.commit()
            flash('Product updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {str(e)}', 'danger')
    
    return render_template('products/form.html', product=product)
```

## Pull Request Process

1. **Branch Naming**
   - `feature/description` for new features
   - `fix/description` for bug fixes
   - `docs/description` for documentation
   - `refactor/description` for code improvements

2. **Commit Messages**
   - Use present tense ("Add feature" not "Added feature")
   - Be concise but descriptive
   - Reference issues when applicable

3. **Before Submitting**
   - Ensure all tests pass
   - Update documentation if needed
   - Add tests for new functionality
   - Check code style

4. **PR Description**
   - Describe what changes were made
   - Explain why the changes were made
   - List any breaking changes
   - Include testing instructions

## Bug Reports

When reporting bugs, please include:

- Clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, browser)
- Screenshots if applicable
- Error logs if available

## Feature Requests

When requesting features, please include:

- Clear description of the feature
- Use case or problem it solves
- Proposed implementation (optional)
- Examples of similar features (if any)

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_products.py

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_products.py::test_create_product
```

## Security

- Never commit sensitive data (passwords, API keys)
- Use environment variables for secrets
- Validate all user input
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Keep dependencies up to date

## Documentation

- Update README.md for significant changes
- Add inline comments for complex logic
- Document API endpoints
- Keep CHANGELOG.md updated

## Questions?

Feel free to open an issue for any questions or concerns.

Thank you for contributing to Ampoulex! 🎉
