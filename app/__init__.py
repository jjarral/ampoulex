# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_mail import Mail
from config import Config
from datetime import datetime, timedelta
import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('ignore', category=SAWarning)

# Initialize extensions (WITHOUT app - this is critical!)
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
mail = Mail()  # ✅ Initialize WITHOUT app at module level

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # ✅ Production-safe configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///ampoulex.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', app.config['SECRET_KEY'])
    
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
    
    with app.app_context():
        db.create_all()
        # Don't create default accounts in production
        if os.environ.get('FLASK_ENV') != 'production':
            create_default_accounts()
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
def create_default_accounts():
    """Create default chart of accounts on first run"""
    from app.models import Account
    
    default_accounts = [
        # Assets
        ('1000', 'Cash', 'Asset', None),
        ('1010', 'Cash in Hand', 'Asset', '1000'),
        ('1020', 'Petty Cash', 'Asset', '1000'),
        ('1100', 'Bank', 'Asset', None),
        ('1110', 'Bank - MCB', 'Asset', '1100'),
        ('1120', 'Bank - HBL', 'Asset', '1100'),
        ('1200', 'Accounts Receivable', 'Asset', None),
        ('1300', 'Inventory', 'Asset', None),
        ('1400', 'Fixed Assets', 'Asset', None),
        
        # Liabilities
        ('2000', 'Liabilities', 'Liability', None),
        ('2100', 'Accounts Payable', 'Liability', '2000'),
        ('2200', 'Tax Payable', 'Liability', '2000'),
        
        # Equity
        ('3000', 'Equity', 'Equity', None),
        ('3100', 'Share Capital', 'Equity', '3000'),
        ('3200', 'Retained Earnings', 'Equity', '3000'),
        
        # Income
        ('4000', 'Income', 'Income', None),
        ('4100', 'Sales Revenue', 'Income', '4000'),
        ('4200', 'Service Revenue', 'Income', '4000'),
        
        # Expenses
        ('5000', 'Expenses', 'Expense', None),
        ('5100', 'Cost of Goods Sold', 'Expense', '5000'),
        ('5200', 'Salaries', 'Expense', '5000'),
        ('5300', 'Rent', 'Expense', '5000'),
        ('5400', 'Utilities', 'Expense', '5000'),
        ('5500', 'Office Expenses', 'Expense', '5000'),
    ]
    
    for code, name, acc_type, parent_code in default_accounts:
        parent_id = None
        if parent_code:
            parent = Account.query.filter_by(account_code=parent_code).first()
            if parent:
                parent_id = parent.id
        
        existing = Account.query.filter_by(account_code=code).first()
        if not existing:
            account = Account(
                account_code=code,
                account_name=name,
                account_type=acc_type,
                parent_account_id=parent_id,
                is_active=True
            )
            db.session.add(account)
    
    db.session.commit()
    print("✅ Default chart of accounts created!")    