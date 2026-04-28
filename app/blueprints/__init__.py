"""
Ampoulex Blueprints Package

This package contains all Flask blueprints organized by business domain.
Each blueprint is responsible for a specific area of functionality.
"""

from app.blueprints.auth import auth_bp
from app.blueprints.products import products_bp
from app.blueprints.orders import orders_bp
from app.blueprints.customers import customers_bp
from app.blueprints.suppliers import suppliers_bp
from app.blueprints.inventory import inventory_bp
from app.blueprints.production import production_bp
from app.blueprints.qc import qc_bp
from app.blueprints.accounting import accounting_bp
from app.blueprints.payroll import payroll_bp
from app.blueprints.reports import reports_bp
from app.blueprints.admin import admin_bp

__all__ = [
    'auth_bp',
    'products_bp',
    'orders_bp',
    'customers_bp',
    'suppliers_bp',
    'inventory_bp',
    'production_bp',
    'qc_bp',
    'accounting_bp',
    'payroll_bp',
    'reports_bp',
    'admin_bp',
]
