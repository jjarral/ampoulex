# Ampoulex ERP System

## Overview
Ampoulex is a comprehensive Enterprise Resource Planning (ERP) / Business Management System built with Flask. It handles accounting, inventory, production, quality control, payroll, and sales operations, configured for a company operating in Pakistan (PKR currency).

## Architecture
- **Backend:** Python Flask 3.0 with SQLAlchemy ORM
- **Database:** PostgreSQL (Replit built-in)
- **Real-time:** Flask-SocketIO with eventlet
- **Frontend:** AdminLTE 4, Bootstrap 5, jQuery, Chart.js, DataTables, SweetAlert2
- **Reporting:** ReportLab (PDF), Openpyxl (Excel), pandas

## Project Structure
```
app/
  __init__.py     - App factory, extension init
  routes.py       - All route handlers (~5300 lines)
  models.py       - SQLAlchemy models
  forms.py        - Flask-WTF forms
  utils/          - Tax calculator and helpers
  email_helper.py - Email utilities
templates/        - 108 Jinja2 templates organized by module
static/           - CSS, JS, images, Excel templates
migrations/       - Alembic DB migrations
run.py            - Entry point (python run.py)
config.py         - Configuration class
```

## Running the App
- **Dev:** `python run.py` → http://localhost:5000
- **Default Login:** admin / admin123
- **Production:** gunicorn with eventlet worker

## Environment Variables
- `DATABASE_URL` - PostgreSQL connection string (auto-set by Replit)
- `SECRET_KEY` - Flask session secret key
- `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` - DB credentials

## Key Modules
- Accounting (chart of accounts, journal entries, bank reconciliation)
- Inventory (warehouses, stock transfers, purchase orders)
- Production (batch management, BOM)
- Quality Control (parameters, CAPA, calibration, COA)
- Payroll (employees, attendance, timesheets, leave)
- Sales (inquiries, orders, customers)
- Reporting & Analytics
- Tax/FBR compliance
- Painting service module
