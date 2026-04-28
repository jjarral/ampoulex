"""
Production Management Blueprint Routes

Handles all production-related HTTP requests including production orders,
batch tracking, work orders, and manufacturing schedules.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

production_bp = Blueprint('production', __name__, url_prefix='/production')

# In-memory storage (replace with database in production)
production_orders_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "order_number": "PO-2024-001",
        "product_id": 1,
        "product_name": "Paracetamol 500mg",
        "quantity": 10000,
        "unit": "boxes",
        "status": "in_progress",
        "start_date": "2024-03-10",
        "end_date": "2024-03-17",
        "batch_number": "BATCH-2024-001",
        "created_at": "2024-03-08"
    },
    {
        "id": 2,
        "order_number": "PO-2024-002",
        "product_id": 2,
        "product_name": "Ibuprofen 200mg",
        "quantity": 8000,
        "unit": "boxes",
        "status": "pending",
        "start_date": "2024-03-18",
        "end_date": "2024-03-25",
        "batch_number": "BATCH-2024-002",
        "created_at": "2024-03-12"
    }
]

work_orders_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "production_order_id": 1,
        "work_center": "Mixing",
        "operation": "Raw Material Mixing",
        "status": "completed",
        "assigned_to": "Team A",
        "start_time": "2024-03-10 08:00",
        "end_time": "2024-03-10 14:00"
    },
    {
        "id": 2,
        "production_order_id": 1,
        "work_center": "Tablet Press",
        "operation": "Tablet Compression",
        "status": "in_progress",
        "assigned_to": "Team B",
        "start_time": "2024-03-11 08:00",
        "end_time": None
    }
]

batches_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "batch_number": "BATCH-2024-001",
        "product_id": 1,
        "product_name": "Paracetamol 500mg",
        "quantity_produced": 5000,
        "quantity_expected": 10000,
        "status": "in_progress",
        "production_date": "2024-03-10",
        "expiry_date": "2026-03-10",
        "qc_status": "pending"
    }
]


@production_bp.route('/')
def index():
    """List all production orders."""
    status_filter = request.args.get('status', '')
    
    filtered_orders = production_orders_db
    
    if status_filter:
        filtered_orders = [o for o in filtered_orders if o['status'] == status_filter]
    
    return render_template('production/index.html', 
                         orders=filtered_orders,
                         status_filter=status_filter)


@production_bp.route('/new')
def new():
    """Display form to create new production order."""
    return render_template('production/new.html')


@production_bp.route('/', methods=['POST'])
def create():
    """Create a new production order."""
    try:
        new_id = max([o['id'] for o in production_orders_db], default=0) + 1
        today = datetime.now()
        
        new_order = {
            "id": new_id,
            "order_number": f"PO-{today.strftime('%Y')}-{new_id:03d}",
            "product_id": int(request.form.get('product_id')),
            "product_name": request.form.get('product_name'),
            "quantity": int(request.form.get('quantity')),
            "unit": request.form.get('unit', 'boxes'),
            "status": "pending",
            "start_date": request.form.get('start_date'),
            "end_date": request.form.get('end_date'),
            "batch_number": f"BATCH-{today.strftime('%Y')}-{new_id:03d}",
            "created_at": today.strftime('%Y-%m-%d')
        }
        
        production_orders_db.append(new_order)
        flash(f'Production Order "{new_order["order_number"]}" created successfully!', 'success')
        return redirect(url_for('production.index'))
    
    except Exception as e:
        flash(f'Error creating production order: {str(e)}', 'danger')
        return render_template('production/new.html'), 400


@production_bp.route('/<int:order_id>')
def show(order_id: int):
    """Display production order details."""
    order = next((o for o in production_orders_db if o['id'] == order_id), None)
    
    if not order:
        flash('Production order not found', 'danger')
        return redirect(url_for('production.index'))
    
    order_work_orders = [wo for wo in work_orders_db if wo['production_order_id'] == order_id]
    order_batch = next((b for b in batches_db if b['batch_number'] == order['batch_number']), None)
    
    return render_template('production/show.html', 
                         order=order,
                         work_orders=order_work_orders,
                         batch=order_batch)


@production_bp.route('/<int:order_id>/edit')
def edit(order_id: int):
    """Display form to edit production order."""
    order = next((o for o in production_orders_db if o['id'] == order_id), None)
    
    if not order:
        flash('Production order not found', 'danger')
        return redirect(url_for('production.index'))
    
    return render_template('production/edit.html', order=order)


@production_bp.route('/<int:order_id>', methods=['PUT'])
def update(order_id: int):
    """Update production order."""
    try:
        order = next((o for o in production_orders_db if o['id'] == order_id), None)
        
        if not order:
            flash('Production order not found', 'danger')
            return redirect(url_for('production.index'))
        
        order['quantity'] = int(request.form.get('quantity', order['quantity']))
        order['status'] = request.form.get('status', order['status'])
        order['start_date'] = request.form.get('start_date', order['start_date'])
        order['end_date'] = request.form.get('end_date', order['end_date'])
        
        flash(f'Production Order "{order["order_number"]}" updated successfully!', 'success')
        return redirect(url_for('production.show', order_id=order_id))
    
    except Exception as e:
        flash(f'Error updating production order: {str(e)}', 'danger')
        return render_template('production/edit.html', order=order), 400


@production_bp.route('/<int:order_id>/start', methods=['POST'])
def start_production(order_id: int):
    """Start a production order."""
    try:
        order = next((o for o in production_orders_db if o['id'] == order_id), None)
        
        if not order:
            flash('Production order not found', 'danger')
            return redirect(url_for('production.index'))
        
        order['status'] = 'in_progress'
        order['start_date'] = datetime.now().strftime('%Y-%m-%d')
        
        flash(f'Production Order "{order["order_number"]}" started!', 'success')
        return redirect(url_for('production.show', order_id=order_id))
    
    except Exception as e:
        flash(f'Error starting production: {str(e)}', 'danger')
        return redirect(url_for('production.show', order_id=order_id))


@production_bp.route('/<int:order_id>/complete', methods=['POST'])
def complete_production(order_id: int):
    """Complete a production order."""
    try:
        order = next((o for o in production_orders_db if o['id'] == order_id), None)
        
        if not order:
            flash('Production order not found', 'danger')
            return redirect(url_for('production.index'))
        
        order['status'] = 'completed'
        order['end_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Update batch
        batch = next((b for b in batches_db if b['batch_number'] == order['batch_number']), None)
        if batch:
            batch['status'] = 'completed'
            batch['quantity_produced'] = order['quantity']
        
        flash(f'Production Order "{order["order_number"]}" completed!', 'success')
        return redirect(url_for('production.show', order_id=order_id))
    
    except Exception as e:
        flash(f'Error completing production: {str(e)}', 'danger')
        return redirect(url_for('production.show', order_id=order_id))


@production_bp.route('/work-orders')
def work_orders():
    """List all work orders."""
    status_filter = request.args.get('status', '')
    
    filtered_orders = work_orders_db
    
    if status_filter:
        filtered_orders = [wo for wo in filtered_orders if wo['status'] == status_filter]
    
    return render_template('production/work_orders.html', 
                         work_orders=filtered_orders,
                         status_filter=status_filter)


@production_bp.route('/work-orders/new', methods=['GET', 'POST'])
def new_work_order():
    """Create a new work order."""
    if request.method == 'GET':
        return render_template('production/new_work_order.html',
                             production_orders=production_orders_db)
    
    try:
        new_id = max([wo['id'] for wo in work_orders_db], default=0) + 1
        
        new_work_order = {
            "id": new_id,
            "production_order_id": int(request.form.get('production_order_id')),
            "work_center": request.form.get('work_center'),
            "operation": request.form.get('operation'),
            "status": "pending",
            "assigned_to": request.form.get('assigned_to'),
            "start_time": request.form.get('start_time'),
            "end_time": None
        }
        
        work_orders_db.append(new_work_order)
        flash('Work Order created successfully!', 'success')
        return redirect(url_for('production.work_orders'))
    
    except Exception as e:
        flash(f'Error creating work order: {str(e)}', 'danger')
        return render_template('production/new_work_order.html'), 400


@production_bp.route('/batches')
def batches():
    """List all batches."""
    status_filter = request.args.get('status', '')
    qc_filter = request.args.get('qc_status', '')
    
    filtered_batches = batches_db
    
    if status_filter:
        filtered_batches = [b for b in filtered_batches if b['status'] == status_filter]
    
    if qc_filter:
        filtered_batches = [b for b in filtered_batches if b['qc_status'] == qc_filter]
    
    return render_template('production/batches.html', 
                         batches=filtered_batches,
                         status_filter=status_filter,
                         qc_filter=qc_filter)


@production_bp.route('/batches/<int:batch_id>')
def show_batch(batch_id: int):
    """Display batch details."""
    batch = next((b for b in batches_db if b['id'] == batch_id), None)
    
    if not batch:
        flash('Batch not found', 'danger')
        return redirect(url_for('production.batches'))
    
    return render_template('production/show_batch.html', batch=batch)


@production_bp.route('/schedule')
def schedule():
    """Display production schedule."""
    # Group orders by date
    schedule_data = {}
    for order in production_orders_db:
        date = order.get('start_date', 'TBD')
        if date not in schedule_data:
            schedule_data[date] = []
        schedule_data[date].append(order)
    
    return render_template('production/schedule.html', schedule=schedule_data)


@production_bp.route('/reports/efficiency')
def efficiency_report():
    """Generate production efficiency report."""
    total_orders = len(production_orders_db)
    completed_orders = len([o for o in production_orders_db if o['status'] == 'completed'])
    in_progress = len([o for o in production_orders_db if o['status'] == 'in_progress'])
    
    efficiency_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0
    
    return render_template('production/reports/efficiency.html',
                         total_orders=total_orders,
                         completed_orders=completed_orders,
                         in_progress=in_progress,
                         efficiency_rate=efficiency_rate)


@production_bp.route('/api/list')
def api_list():
    """API endpoint to list production orders."""
    return jsonify({
        'success': True,
        'data': production_orders_db,
        'count': len(production_orders_db)
    })


@production_bp.route('/api/<int:order_id>')
def api_show(order_id: int):
    """API endpoint to get production order details."""
    order = next((o for o in production_orders_db if o['id'] == order_id), None)
    
    if not order:
        return jsonify({'success': False, 'error': 'Order not found'}), 404
    
    return jsonify({'success': True, 'data': order})
