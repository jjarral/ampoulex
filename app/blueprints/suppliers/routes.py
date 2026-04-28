"""
Supplier Management Blueprint Routes

Handles all supplier-related HTTP requests including CRUD operations,
purchase orders, and supplier performance tracking.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from typing import Dict, List, Any, Optional
from datetime import datetime

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')

# In-memory storage (replace with database in production)
suppliers_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Global Pharma Supplies",
        "contact_person": "John Smith",
        "email": "john@globalpharma.com",
        "phone": "+1-555-0101",
        "address": "123 Supply Chain Blvd, NY 10001",
        "status": "active",
        "rating": 4.8,
        "created_at": "2024-01-15"
    },
    {
        "id": 2,
        "name": "MediPack Industries",
        "contact_person": "Sarah Johnson",
        "email": "sarah@medipack.com",
        "phone": "+1-555-0102",
        "address": "456 Industrial Park, CA 90210",
        "status": "active",
        "rating": 4.5,
        "created_at": "2024-02-20"
    }
]

purchase_orders_db: List[Dict[str, Any]] = []


@suppliers_bp.route('/')
def index():
    """List all suppliers."""
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    filtered_suppliers = suppliers_db
    
    if search:
        filtered_suppliers = [
            s for s in filtered_suppliers 
            if search.lower() in s['name'].lower() or search.lower() in s.get('contact_person', '').lower()
        ]
    
    if status_filter:
        filtered_suppliers = [s for s in filtered_suppliers if s['status'] == status_filter]
    
    return render_template('suppliers/index.html', 
                         suppliers=filtered_suppliers,
                         search=search,
                         status_filter=status_filter)


@suppliers_bp.route('/new')
def new():
    """Display form to create new supplier."""
    return render_template('suppliers/new.html')


@suppliers_bp.route('/', methods=['POST'])
def create():
    """Create a new supplier."""
    try:
        new_id = max([s['id'] for s in suppliers_db], default=0) + 1
        
        new_supplier = {
            "id": new_id,
            "name": request.form.get('name'),
            "contact_person": request.form.get('contact_person'),
            "email": request.form.get('email'),
            "phone": request.form.get('phone'),
            "address": request.form.get('address'),
            "status": "active",
            "rating": 0.0,
            "created_at": datetime.now().strftime('%Y-%m-%d')
        }
        
        suppliers_db.append(new_supplier)
        flash(f'Supplier "{new_supplier["name"]}" created successfully!', 'success')
        return redirect(url_for('suppliers.index'))
    
    except Exception as e:
        flash(f'Error creating supplier: {str(e)}', 'danger')
        return render_template('suppliers/new.html'), 400


@suppliers_bp.route('/<int:supplier_id>')
def show(supplier_id: int):
    """Display supplier details."""
    supplier = next((s for s in suppliers_db if s['id'] == supplier_id), None)
    
    if not supplier:
        flash('Supplier not found', 'danger')
        return redirect(url_for('suppliers.index'))
    
    supplier_orders = [po for po in purchase_orders_db if po['supplier_id'] == supplier_id]
    
    return render_template('suppliers/show.html', 
                         supplier=supplier,
                         purchase_orders=supplier_orders)


@suppliers_bp.route('/<int:supplier_id>/edit')
def edit(supplier_id: int):
    """Display form to edit supplier."""
    supplier = next((s for s in suppliers_db if s['id'] == supplier_id), None)
    
    if not supplier:
        flash('Supplier not found', 'danger')
        return redirect(url_for('suppliers.index'))
    
    return render_template('suppliers/edit.html', supplier=supplier)


@suppliers_bp.route('/<int:supplier_id>', methods=['PUT'])
def update(supplier_id: int):
    """Update supplier information."""
    try:
        supplier = next((s for s in suppliers_db if s['id'] == supplier_id), None)
        
        if not supplier:
            flash('Supplier not found', 'danger')
            return redirect(url_for('suppliers.index'))
        
        supplier['name'] = request.form.get('name')
        supplier['contact_person'] = request.form.get('contact_person')
        supplier['email'] = request.form.get('email')
        supplier['phone'] = request.form.get('phone')
        supplier['address'] = request.form.get('address')
        supplier['status'] = request.form.get('status', 'active')
        
        flash(f'Supplier "{supplier["name"]}" updated successfully!', 'success')
        return redirect(url_for('suppliers.show', supplier_id=supplier_id))
    
    except Exception as e:
        flash(f'Error updating supplier: {str(e)}', 'danger')
        return render_template('suppliers/edit.html', supplier=supplier), 400


@suppliers_bp.route('/<int:supplier_id>', methods=['DELETE'])
def delete(supplier_id: int):
    """Delete a supplier."""
    try:
        supplier = next((s for s in suppliers_db if s['id'] == supplier_id), None)
        
        if not supplier:
            flash('Supplier not found', 'danger')
            return redirect(url_for('suppliers.index'))
        
        suppliers_db.remove(supplier)
        flash(f'Supplier "{supplier["name"]}" deleted successfully!', 'success')
        return redirect(url_for('suppliers.index'))
    
    except Exception as e:
        flash(f'Error deleting supplier: {str(e)}', 'danger')
        return redirect(url_for('suppliers.show', supplier_id=supplier_id))


@suppliers_bp.route('/<int:supplier_id>/orders')
def purchase_orders(supplier_id: int):
    """List purchase orders for a supplier."""
    supplier = next((s for s in suppliers_db if s['id'] == supplier_id), None)
    
    if not supplier:
        flash('Supplier not found', 'danger')
        return redirect(url_for('suppliers.index'))
    
    supplier_orders = [po for po in purchase_orders_db if po['supplier_id'] == supplier_id]
    
    return render_template('suppliers/orders.html', 
                         supplier=supplier,
                         purchase_orders=supplier_orders)


@suppliers_bp.route('/<int:supplier_id>/orders/new')
def new_purchase_order(supplier_id: int):
    """Display form to create new purchase order."""
    supplier = next((s for s in suppliers_db if s['id'] == supplier_id), None)
    
    if not supplier:
        flash('Supplier not found', 'danger')
        return redirect(url_for('suppliers.index'))
    
    return render_template('suppliers/new_order.html', supplier=supplier)


@suppliers_bp.route('/<int:supplier_id>/orders', methods=['POST'])
def create_purchase_order(supplier_id: int):
    """Create a new purchase order."""
    try:
        supplier = next((s for s in suppliers_db if s['id'] == supplier_id), None)
        
        if not supplier:
            flash('Supplier not found', 'danger')
            return redirect(url_for('suppliers.index'))
        
        new_id = max([po['id'] for po in purchase_orders_db], default=0) + 1
        
        new_order = {
            "id": new_id,
            "supplier_id": supplier_id,
            "order_number": f"PO-{datetime.now().strftime('%Y%m%d')}-{new_id:04d}",
            "items": [],  # Parse from form
            "total_amount": float(request.form.get('total_amount', 0)),
            "status": "pending",
            "expected_delivery": request.form.get('expected_delivery'),
            "notes": request.form.get('notes'),
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        purchase_orders_db.append(new_order)
        flash(f'Purchase Order "{new_order["order_number"]}" created successfully!', 'success')
        return redirect(url_for('suppliers.purchase_orders', supplier_id=supplier_id))
    
    except Exception as e:
        flash(f'Error creating purchase order: {str(e)}', 'danger')
        return redirect(url_for('suppliers.new_purchase_order', supplier_id=supplier_id))


@suppliers_bp.route('/performance')
def performance():
    """Display supplier performance metrics."""
    metrics = []
    
    for supplier in suppliers_db:
        supplier_orders = [po for po in purchase_orders_db if po['supplier_id'] == supplier['id']]
        total_orders = len(supplier_orders)
        pending_orders = len([po for po in supplier_orders if po['status'] == 'pending'])
        
        metrics.append({
            'supplier': supplier,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'on_time_rate': supplier.get('rating', 0)
        })
    
    return render_template('suppliers/performance.html', metrics=metrics)


@suppliers_bp.route('/api/list')
def api_list():
    """API endpoint to list suppliers."""
    return jsonify({
        'success': True,
        'data': suppliers_db,
        'count': len(suppliers_db)
    })


@suppliers_bp.route('/api/<int:supplier_id>')
def api_show(supplier_id: int):
    """API endpoint to get supplier details."""
    supplier = next((s for s in suppliers_db if s['id'] == supplier_id), None)
    
    if not supplier:
        return jsonify({'success': False, 'error': 'Supplier not found'}), 404
    
    return jsonify({'success': True, 'data': supplier})
