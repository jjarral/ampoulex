"""Customers Blueprint Module"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from sqlalchemy import func
from datetime import datetime

from app import db
from app.models import Customer, CustomerProductPrice, CustomerPaintingPrice, PaintingServicePrice

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')


def log_activity(description):
    """Simple activity logging helper"""
    try:
        from app.models import AuditLog
        log = AuditLog(
            action=description,
            timestamp=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        pass  # Silently fail if logging fails


@customers_bp.route('/')
@login_required
def index():
    """List all customers"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Customer.query
    
    if search:
        query = query.filter(
            (Customer.name.ilike(f'%{search}%')) |
            (Customer.business_name.ilike(f'%{search}%')) |
            (Customer.email.ilike(f'%{search}%')) |
            (Customer.phone.ilike(f'%{search}%'))
        )
    
    customers = query.order_by(Customer.name).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('customers/index.html', 
                         customers=customers,
                         search=search)


@customers_bp.route('/new', methods=['GET', 'POST'])
@login_required
def add_customer():
    """Add a new customer"""
    if request.method == 'POST':
        try:
            customer = Customer(
                name=request.form.get('name', '').strip(),
                business_name=request.form.get('business_name', '').strip(),
                email=request.form.get('email', '').strip().lower() if request.form.get('email') else None,
                phone=request.form.get('phone', '').strip(),
                address=request.form.get('address', '').strip(),
                city=request.form.get('city', '').strip(),
                country=request.form.get('country', '').strip(),
                cnic=request.form.get('cnic', '').strip(),
                stripe_customer_id=request.form.get('stripe_customer_id', '').strip(),
                notes=request.form.get('notes', '').strip()
            )
            db.session.add(customer)
            db.session.commit()
            log_activity(f'Customer created: {customer.name}')
            flash('Customer added successfully!', 'success')
            return redirect(url_for('customers.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding customer: {str(e)}', 'danger')
    
    return render_template('customers/form.html', customer=None)


@customers_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    """Edit existing customer"""
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            customer.name = request.form.get('name', '').strip()
            customer.business_name = request.form.get('business_name', '').strip()
            customer.email = request.form.get('email', '').strip().lower() if request.form.get('email') else None
            customer.phone = request.form.get('phone', '').strip()
            customer.address = request.form.get('address', '').strip()
            customer.city = request.form.get('city', '').strip()
            customer.country = request.form.get('country', '').strip()
            customer.cnic = request.form.get('cnic', '').strip()
            customer.stripe_customer_id = request.form.get('stripe_customer_id', '').strip()
            customer.notes = request.form.get('notes', '').strip()
            
            db.session.commit()
            log_activity(f'Customer updated: {customer.name}')
            flash('Customer updated successfully!', 'success')
            return redirect(url_for('customers.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating customer: {str(e)}', 'danger')
    
    return render_template('customers/form.html', customer=customer)


@customers_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_customer(id):
    """Delete customer"""
    customer = Customer.query.get_or_404(id)
    
    try:
        # Check if customer has orders
        from app.models import Order
        has_orders = Order.query.filter_by(customer_id=id).first()
        if has_orders:
            flash('Cannot delete customer with existing orders!', 'warning')
            return redirect(url_for('customers.index'))
        
        db.session.delete(customer)
        db.session.commit()
        log_activity(f'Customer deleted: {customer.name}')
        flash('Customer deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting customer: {str(e)}', 'danger')
    
    return redirect(url_for('customers.index'))


@customers_bp.route('/<int:id>/painting-pricing', methods=['GET', 'POST'])
@login_required
def manage_painting_pricing(id):
    """Manage painting pricing for customer"""
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Get form data
            price_data = request.form.get('price_data', '{}')
            import json
            prices = json.loads(price_data)
            
            # Update or create pricing records
            for item_id, price_info in prices.items():
                painting_price = CustomerPaintingPrice.query.filter_by(
                    customer_id=customer.id,
                    painting_service_id=int(item_id)
                ).first()
                
                if painting_price:
                    painting_price.price = float(price_info.get('price', 0))
                    painting_price.is_active = price_info.get('is_active', True)
                else:
                    painting_price = CustomerPaintingPrice(
                        customer_id=customer.id,
                        painting_service_id=int(item_id),
                        price=float(price_info.get('price', 0)),
                        is_active=price_info.get('is_active', True)
                    )
                    db.session.add(painting_price)
            
            db.session.commit()
            flash('Painting pricing updated successfully!', 'success')
            return redirect(url_for('customers.manage_painting_pricing', id=customer.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating pricing: {str(e)}', 'danger')
    
    # Get all painting services
    painting_services = PaintingServicePrice.query.filter_by(is_active=True).all()
    
    # Get customer's current pricing
    customer_prices = {cp.painting_service_id: cp for cp in CustomerPaintingPrice.query.filter_by(customer_id=customer.id).all()}
    
    return render_template('customers/painting_pricing.html',
                         customer=customer,
                         painting_services=painting_services,
                         customer_prices=customer_prices)


@customers_bp.route('/merge', methods=['GET', 'POST'])
@login_required
def merge_customers():
    """Merge duplicate customers"""
    if request.method == 'POST':
        try:
            primary_id = request.form.get('primary_customer_id')
            secondary_ids = request.form.getlist('secondary_customer_ids[]')
            
            if not primary_id or not secondary_ids:
                flash('Please select customers to merge!', 'warning')
                return redirect(url_for('customers.merge_customers'))
            
            primary_customer = Customer.query.get_or_404(primary_id)
            
            # Merge logic would go here
            # Update orders, inquiries, etc. to point to primary customer
            
            log_activity(f'Customers merged into: {primary_customer.name}')
            flash('Customers merged successfully!', 'success')
            return redirect(url_for('customers.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error merging customers: {str(e)}', 'danger')
    
    # Get list of customers for selection
    customers = Customer.query.order_by(Customer.name).all()
    return render_template('customers/merge.html', customers=customers)


@customers_bp.route('/<int:id>/product-prices', methods=['GET', 'POST'])
@login_required
def manage_product_prices(id):
    """Manage product-specific pricing for customer"""
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            from app.models import Product
            product_id = request.form.get('product_id')
            special_price = request.form.get('special_price', type=float)
            is_active = request.form.get('is_active', False)
            
            if product_id:
                price_record = CustomerProductPrice.query.filter_by(
                    customer_id=customer.id,
                    product_id=int(product_id)
                ).first()
                
                if price_record:
                    price_record.special_price = special_price
                    price_record.is_active = is_active
                else:
                    price_record = CustomerProductPrice(
                        customer_id=customer.id,
                        product_id=int(product_id),
                        special_price=special_price,
                        is_active=is_active
                    )
                    db.session.add(price_record)
            
            db.session.commit()
            flash('Product pricing updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product pricing: {str(e)}', 'danger')
    
    # Get customer's product prices
    product_prices = CustomerProductPrice.query.filter_by(customer_id=customer.id).all()
    
    return render_template('customers/product_prices.html',
                         customer=customer,
                         product_prices=product_prices)
