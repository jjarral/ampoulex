"""Orders Blueprint Module"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from datetime import datetime
from sqlalchemy import func

from app import db
from app.models import Order, OrderItem, Customer, Product, CustomerProductPrice

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


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


@orders_bp.route('/')
@login_required
def index():
    """List all orders"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    
    if search:
        query = query.filter(
            (Order.order_number.ilike(f'%{search}%')) |
            (Order.customer_name_snapshot.ilike(f'%{search}%'))
        )
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('orders/index.html',
                         orders=orders,
                         current_status=status,
                         search=search)


@orders_bp.route('/new', methods=['GET', 'POST'])
@login_required
def add_order():
    """Add a new order"""
    if request.method == 'POST':
        try:
            customer_id = request.form.get('customer_id', type=int)
            customer = Customer.query.get_or_404(customer_id)
            
            # Create order
            order = Order(
                customer_id=customer.id,
                customer_name_snapshot=customer.name,
                status='pending',
                payment_status='unpaid',
                notes=request.form.get('notes', '').strip()
            )
            db.session.add(order)
            db.session.flush()
            
            # Add order items
            product_ids = request.form.getlist('product_ids[]')
            quantities = request.form.getlist('quantities[]')
            prices = request.form.getlist('prices[]')
            
            for i, product_id in enumerate(product_ids):
                if product_id and quantities[i]:
                    product = Product.query.get(int(product_id))
                    if product:
                        # Check for customer-specific pricing
                        customer_price = CustomerProductPrice.query.filter_by(
                            customer_id=customer.id,
                            product_id=product.id,
                            is_active=True
                        ).first()
                        
                        unit_price = float(prices[i]) if prices[i] else product.base_price
                        if customer_price:
                            unit_price = customer_price.special_price
                        
                        order_item = OrderItem(
                            order_id=order.id,
                            product_id=product.id,
                            quantity=int(quantities[i]),
                            unit_price=unit_price
                        )
                        db.session.add(order_item)
            
            # Calculate total
            order.total_amount = sum(item.quantity * item.unit_price for item in order.items)
            
            db.session.commit()
            log_activity(f'Order created: {order.order_number}')
            flash('Order created successfully!', 'success')
            return redirect(url_for('orders.view', id=order.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating order: {str(e)}', 'danger')
    
    # Get customers and products for form
    customers = Customer.query.order_by(Customer.name).all()
    products = Product.query.filter_by(is_deleted=False).order_by(Product.name).all()
    
    return render_template('orders/form.html',
                         customers=customers,
                         products=products,
                         order=None)


@orders_bp.route('/<int:id>')
@login_required
def view(id):
    """View order details"""
    order = Order.query.get_or_404(id)
    return render_template('orders/view.html', order=order)


@orders_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit existing order"""
    order = Order.query.get_or_404(id)
    
    if order.status in ['completed', 'cancelled']:
        flash('Cannot edit completed or cancelled orders!', 'warning')
        return redirect(url_for('orders.view', id=order.id))
    
    if request.method == 'POST':
        try:
            order.notes = request.form.get('notes', '').strip()
            order.status = request.form.get('status', 'pending')
            
            # Update items
            # Clear existing items
            OrderItem.query.filter_by(order_id=order.id).delete()
            
            product_ids = request.form.getlist('product_ids[]')
            quantities = request.form.getlist('quantities[]')
            prices = request.form.getlist('prices[]')
            
            for i, product_id in enumerate(product_ids):
                if product_id and quantities[i]:
                    product = Product.query.get(int(product_id))
                    if product:
                        order_item = OrderItem(
                            order_id=order.id,
                            product_id=product.id,
                            quantity=int(quantities[i]),
                            unit_price=float(prices[i]) if prices[i] else product.base_price
                        )
                        db.session.add(order_item)
            
            order.total_amount = sum(item.quantity * item.unit_price for item in order.items)
            
            db.session.commit()
            log_activity(f'Order updated: {order.order_number}')
            flash('Order updated successfully!', 'success')
            return redirect(url_for('orders.view', id=order.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating order: {str(e)}', 'danger')
    
    customers = Customer.query.order_by(Customer.name).all()
    products = Product.query.filter_by(is_deleted=False).order_by(Product.name).all()
    
    return render_template('orders/edit.html',
                         order=order,
                         customers=customers,
                         products=products)


@orders_bp.route('/<int:id>/invoice')
@login_required
def invoice(id):
    """Generate order invoice"""
    order = Order.query.get_or_404(id)
    return render_template('orders/invoice.html', order=order)


@orders_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete order"""
    order = Order.query.get_or_404(id)
    
    if order.status == 'completed':
        flash('Cannot delete completed orders!', 'warning')
        return redirect(url_for('orders.index'))
    
    try:
        order_number = order.order_number
        db.session.delete(order)
        db.session.commit()
        log_activity(f'Order deleted: {order_number}')
        flash('Order deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting order: {str(e)}', 'danger')
    
    return redirect(url_for('orders.index'))


@orders_bp.route('/<int:id>/complete', methods=['POST'])
@login_required
def complete(id):
    """Mark order as completed"""
    order = Order.query.get_or_404(id)
    
    try:
        order.status = 'completed'
        order.completed_at = datetime.utcnow()
        
        # Deduct stock
        for item in order.items:
            if item.product:
                item.product.stock -= item.quantity
        
        db.session.commit()
        log_activity(f'Order completed: {order.order_number}')
        flash('Order marked as completed!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error completing order: {str(e)}', 'danger')
    
    return redirect(url_for('orders.view', id=order.id))


@orders_bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    """Cancel order"""
    order = Order.query.get_or_404(id)
    
    try:
        order.status = 'cancelled'
        db.session.commit()
        log_activity(f'Order cancelled: {order.order_number}')
        flash('Order cancelled!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error cancelling order: {str(e)}', 'danger')
    
    return redirect(url_for('orders.view', id=order.id))
