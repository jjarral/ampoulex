#!/usr/bin/env python
"""
Ampoulex Database Updater
Creates/updates all database tables with new models
"""

import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import create_app, db
from app.models import User, Product, Customer, Inquiry, Order, Employee, Expense, Attendance, Timesheet, LeaveRequest, PayrollPayment
from werkzeug.security import generate_password_hash


def main():
    print("=" * 60)
    print("Ampoulex Database Updater")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        print("\nCreating/updating database tables...")
        
        # This creates all tables defined in models.py
        # Existing tables are updated, new ones are created
        db.create_all()
        
        print("[OK] Database schema updated!")
        
        # List all tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\nFound {len(tables)} tables:")
        for table in sorted(tables):
            print(f"  - {table}")
        
        # Show record counts
        print("\nRecord counts:")
        print("\nRecord counts:")
        print(f"  - Users: {User.query.count()}")
        print(f"  - Products: {Product.query.count()}")
        print(f"  - Customers: {Customer.query.count()}")
        print(f"  - Inquiries: {Inquiry.query.count()}")
        print(f"  - Orders: {Order.query.count()}")
        print(f"  - Employees: {Employee.query.count()}")
        print(f"  - Attendance Records: {Attendance.query.count()}")
        print(f"  - Timesheets: {Timesheet.query.count()}")
        print(f"  - Leave Requests: {LeaveRequest.query.count()}")
        print(f"  - Payroll Payments: {PayrollPayment.query.count()}")
        
        # Create default admin if none exists
        if User.query.count() == 0:
            admin = User(
                username='admin',
                email='admin@ampoulex.pk',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("\n[OK] Created default admin user:")
            print("  Username: admin")
            print("  Password: admin123")
        else:
            print("\n[OK] Admin user already exists")
        
        # Create initial products if none exist
        if Product.query.count() == 0:
            print("\nCreating initial products...")
            products_data = [
                {'name': 'Glass Ampoule 1cc', 'specification': '1ml capacity', 'base_price': 25, 'stock': 50000, 'color': 'Transparent', 'product_type': 'product'},
                {'name': 'Glass Ampoule 1cc', 'specification': '1ml capacity', 'base_price': 28, 'stock': 30000, 'color': 'Amber', 'product_type': 'product'},
                {'name': 'Glass Ampoule 2cc', 'specification': '2ml capacity', 'base_price': 35, 'stock': 45000, 'color': 'Transparent', 'product_type': 'product'},
                {'name': 'Glass Ampoule 2cc', 'specification': '2ml capacity', 'base_price': 38, 'stock': 25000, 'color': 'Amber', 'product_type': 'product'},
                {'name': 'Glass Ampoule 3cc', 'specification': '3ml capacity', 'base_price': 42, 'stock': 40000, 'color': 'Transparent', 'product_type': 'product'},
                {'name': 'Glass Ampoule 3cc', 'specification': '3ml capacity', 'base_price': 45, 'stock': 20000, 'color': 'Amber', 'product_type': 'product'},
                {'name': 'Glass Ampoule 5cc', 'specification': '5ml capacity', 'base_price': 50, 'stock': 35000, 'color': 'Transparent', 'product_type': 'product'},
                {'name': 'Glass Ampoule 5cc', 'specification': '5ml capacity', 'base_price': 55, 'stock': 18000, 'color': 'Amber', 'product_type': 'product'},
                {'name': 'Glass Ampoule 10cc', 'specification': '10ml capacity', 'base_price': 65, 'stock': 30000, 'color': 'Transparent', 'product_type': 'product'},
                {'name': 'Glass Ampoule 10cc', 'specification': '10ml capacity', 'base_price': 70, 'stock': 15000, 'color': 'Amber', 'product_type': 'product'},
                {'name': 'White Label Service', 'specification': 'Custom packaging & labeling', 'base_price': 500, 'stock': 0, 'color': 'Custom', 'product_type': 'service'},
            ]
            
            for prod in products_data:
                product = Product(**prod)
                db.session.add(product)
            
            db.session.commit()
            print(f"[OK] Created {len(products_data)} initial products")
        
        print("\n" + "=" * 60)
        print("Database update complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Start the app: python run.py")
        print("  2. Open browser: http://localhost:5000")
        print("  3. Login: admin / admin123")
        print("\n")

if __name__ == '__main__':
    main()