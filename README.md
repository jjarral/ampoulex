# Ampoulex - Business Management ERP

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A comprehensive Enterprise Resource Planning (ERP) system designed for ampoule manufacturing businesses. Built with Flask, PostgreSQL, and modern web technologies.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Modules](#modules)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Modules
- **Product Management** - Complete product catalog with BOM (Bill of Materials)
- **Order Management** - Sales orders, invoices, and tracking
- **Customer Management** - CRM with purchase history
- **Supplier Management** - Vendor management and purchase orders
- **Inventory Management** - Multi-warehouse stock tracking
- **Production** - Batch tracking and material consumption
- **Quality Control** - QC parameters, results, and complaints
- **Accounting** - Full double-entry accounting system
- **Financial Reports** - P&L, Balance Sheet, Cash Flow
- **HR & Payroll** - Employee management, attendance, payroll
- **Expense Tracking** - Expense management and reporting
- **Fixed Assets** - Asset tracking and depreciation
- **Tax/FBR Integration** - Tax compliance and reporting
- **Painting Services** - Special painting order module

### Technical Features
- Real-time updates with Socket.IO
- Role-based access control
- Responsive AdminLTE UI
- PDF report generation
- Barcode & QR code generation
- Excel import/export
- Email notifications
- Audit logging
- Database migrations

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11+, Flask 3.0.0 |
| **Database** | PostgreSQL 13+ |
| **ORM** | SQLAlchemy 3.1.1 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **UI Framework** | AdminLTE 3.2, Bootstrap 5 |
| **Charts** | Chart.js 4.5 |
| **Tables** | DataTables 2.3 |
| **Icons** | Font Awesome 6.4 |
| **Notifications** | SweetAlert2 11 |
| **Real-time** | Flask-SocketIO 5.3.6 |
| **Deployment** | Docker, Gunicorn, Eventlet |

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 13 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/jjarral/ampoulex.git
cd ampoulex
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 5. Create Database
```bash
createdb ampoulex_db
```

### 6. Run Migrations
```bash
flask db upgrade
```

### 7. Start Development Server
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

**Default Login:**
- Username: `admin`
- Password: `admin123`

## 📦 Installation

### Local Development

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for frontend assets)
npm install

# Set up database
createdb ampoulex_db

# Run migrations
flask db upgrade

# Start server
python run.py
```

### Docker Deployment

```bash
# Build Docker image
docker build -t ampoulex .

# Run container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/ampoulex \
  -e SECRET_KEY=your-secret-key \
  ampoulex
```

### Docker Compose

```bash
docker-compose up --build
```

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required
SECRET_KEY=your-super-secret-key-min-32-chars
DATABASE_URL=postgresql://user:pass@localhost:5432/ampoulex_db

# Optional
FLASK_ENV=production
PORT=8080
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
ENABLE_SOCKETIO=True
```

See `.env.example` for all available options.

### Database Configuration

The application supports PostgreSQL with SSL:

```bash
# Local development
DATABASE_URL=postgresql://localhost:5432/ampoulex_db

# Production (Neon, Cloud SQL, etc.)
DATABASE_URL=postgresql://user:pass@host:5432/ampoulex?sslmode=require
```

## 🌐 Deployment

### Google Cloud Run

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/ampoulex

# Deploy to Cloud Run
gcloud run deploy ampoulex \
  --image gcr.io/PROJECT-ID/ampoulex \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Docker Swarm / Kubernetes

See `docker-compose.yml` and `cloudbuild.yaml` for configuration examples.

### Traditional Server

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:8080 \
  --worker-class eventlet \
  --workers 1 \
  wsgi:application
```

## 📁 Project Structure

```
ampoulex/
├── app/                      # Main application package
│   ├── __init__.py          # App factory & extensions
│   ├── models.py            # Database models (1300+ lines)
│   ├── routes.py            # Route handlers (6000+ lines)
│   ├── forms.py             # WTForms forms
│   ├── utils.py             # Utility functions
│   ├── email_helper.py      # Email functionality
│   └── utils/
│       └── tax_calculator.py
├── templates/               # Jinja2 templates (100+)
│   ├── base.html           # Base template
│   ├── dashboard.html      # Main dashboard
│   ├── auth/               # Authentication
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
│   ├── *.png               # Logos and icons
│   └── templates/          # Report templates
├── tests/                   # Test suite
│   ├── conftest.py        # Pytest fixtures
│   ├── test_auth.py       # Auth tests
│   └── test_products.py   # Product tests
├── migrations/              # Database migrations
├── scripts/                 # Deployment scripts
├── backups/                 # Database backups
├── artifacts/               # Design mockups
├── .env.example            # Environment template
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
├── wsgi.py                 # WSGI entry point
└── run.py                  # Development server
```

## 📊 Modules Overview

| Module | Description | Routes |
|--------|-------------|--------|
| Products | Product catalog, BOM, pricing | `/products` |
| Orders | Sales orders, invoices | `/orders` |
| Customers | CRM, pricing, history | `/customers` |
| Suppliers | Vendor management | `/suppliers` |
| Purchase Orders | PO creation, receiving | `/purchase-orders` |
| Warehouses | Stock management | `/warehouses` |
| Production | Batch tracking | `/production` |
| QC | Quality control | `/qc` |
| Accounting | Full accounting | `/accounting` |
| Financials | Financial reports | `/financials` |
| Payroll | HR & payroll | `/payroll` |
| Expenses | Expense tracking | `/expenses` |
| Assets | Fixed assets | `/assets` |
| Tax | FBR integration | `/tax` |
| Painting | Painting services | `/painting` |

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_products.py::test_create_product
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Write/update tests
5. Run tests: `pytest`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

## 🔒 Security

- Never commit `.env` files
- Use strong passwords
- Keep dependencies updated
- Enable HTTPS in production
- Regularly backup your database

---

**Built with ❤️ using Flask and PostgreSQL**