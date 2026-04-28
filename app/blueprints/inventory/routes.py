"""
Inventory Management Blueprint Routes

Handles all inventory-related HTTP requests including stock tracking,
warehouses, stock movements, and inventory adjustments.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from typing import Dict, List, Any, Optional
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

# In-memory storage (replace with database in production)
warehouses_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Main Warehouse",
        "location": "Building A, Floor 1",
        "capacity": 10000,
        "current_stock": 7500,
        "manager": "Mike Wilson",
        "status": "active"
    },
    {
        "id": 2,
        "name": "Cold Storage",
        "location": "Building B, Basement",
        "capacity": 5000,
        "current_stock": 3200,
        "manager": "Lisa Chen",
        "status": "active"
    }
]

stock_items_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "warehouse_id": 1,
        "product_id": 1,
        "product_name": "Paracetamol 500mg",
        "quantity": 5000,
        "unit": "boxes",
        "reorder_level": 1000,
        "last_updated": "2024-03-15"
    },
    {
        "id": 2,
        "warehouse_id": 1,
        "product_id": 2,
        "product_name": "Ibuprofen 200mg",
        "quantity": 3500,
        "unit": "boxes",
        "reorder_level": 800,
        "last_updated": "2024-03-14"
    },
    {
        "id": 3,
        "warehouse_id": 2,
        "product_id": 3,
        "product_name": "Insulin Vials",
        "quantity": 1200,
        "unit": "vials",
        "reorder_level": 300,
        "last_updated": "2024-03-15"
    }
]

stock_movements_db: List[Dict[str, Any]] = []


@inventory_bp.route('/')
def index():
    """List all inventory items."""
    warehouse_filter = request.args.get('warehouse', '')
    low_stock = request.args.get('low_stock', '')
    
    filtered_items = stock_items_db
    
    if warehouse_filter:
        filtered_items = [i for i in filtered_items if str(i['warehouse_id']) == warehouse_filter]
    
    if low_stock:
        filtered_items = [i for i in filtered_items if i['quantity'] <= i['reorder_level']]
    
    return render_template('inventory/index.html', 
                         items=filtered_items,
                         warehouses=warehouses_db,
                         warehouse_filter=warehouse_filter,
                         low_stock=low_stock)


@inventory_bp.route('/warehouses')
def warehouses():
    """List all warehouses."""
    return render_template('inventory/warehouses.html', warehouses=warehouses_db)


@inventory_bp.route('/warehouses/new')
def new_warehouse():
    """Display form to create new warehouse."""
    return render_template('inventory/new_warehouse.html')


@inventory_bp.route('/warehouses', methods=['POST'])
def create_warehouse():
    """Create a new warehouse."""
    try:
        new_id = max([w['id'] for w in warehouses_db], default=0) + 1
        
        new_warehouse = {
            "id": new_id,
            "name": request.form.get('name'),
            "location": request.form.get('location'),
            "capacity": int(request.form.get('capacity', 0)),
            "current_stock": 0,
            "manager": request.form.get('manager'),
            "status": "active"
        }
        
        warehouses_db.append(new_warehouse)
        flash(f'Warehouse "{new_warehouse["name"]}" created successfully!', 'success')
        return redirect(url_for('inventory.warehouses'))
    
    except Exception as e:
        flash(f'Error creating warehouse: {str(e)}', 'danger')
        return render_template('inventory/new_warehouse.html'), 400


@inventory_bp.route('/warehouses/<int:warehouse_id>')
def show_warehouse(warehouse_id: int):
    """Display warehouse details and stock."""
    warehouse = next((w for w in warehouses_db if w['id'] == warehouse_id), None)
    
    if not warehouse:
        flash('Warehouse not found', 'danger')
        return redirect(url_for('inventory.warehouses'))
    
    warehouse_items = [i for i in stock_items_db if i['warehouse_id'] == warehouse_id]
    
    return render_template('inventory/show_warehouse.html', 
                         warehouse=warehouse,
                         items=warehouse_items)


@inventory_bp.route('/adjustments')
def adjustments():
    """List stock adjustments."""
    return render_template('inventory/adjustments.html', movements=stock_movements_db)


@inventory_bp.route('/adjustments/new')
def new_adjustment():
    """Display form to create stock adjustment."""
    return render_template('inventory/new_adjustment.html', 
                         items=stock_items_db,
                         warehouses=warehouses_db)


@inventory_bp.route('/adjustments', methods=['POST'])
def create_adjustment():
    """Create a stock adjustment."""
    try:
        item_id = int(request.form.get('item_id'))
        quantity_change = int(request.form.get('quantity_change'))
        reason = request.form.get('reason')
        
        item = next((i for i in stock_items_db if i['id'] == item_id), None)
        
        if not item:
            flash('Item not found', 'danger')
            return redirect(url_for('inventory.adjustments'))
        
        old_quantity = item['quantity']
        item['quantity'] += quantity_change
        item['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        
        movement = {
            "id": len(stock_movements_db) + 1,
            "item_id": item_id,
            "product_name": item['product_name'],
            "warehouse_id": item['warehouse_id'],
            "movement_type": "adjustment",
            "quantity_change": quantity_change,
            "old_quantity": old_quantity,
            "new_quantity": item['quantity'],
            "reason": reason,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        stock_movements_db.append(movement)
        
        action = "increased" if quantity_change > 0 else "decreased"
        flash(f'Stock {action} by {abs(quantity_change)} units successfully!', 'success')
        return redirect(url_for('inventory.index'))
    
    except Exception as e:
        flash(f'Error creating adjustment: {str(e)}', 'danger')
        return render_template('inventory/new_adjustment.html'), 400


@inventory_bp.route('/transfers')
def transfers():
    """List stock transfers between warehouses."""
    transfer_movements = [m for m in stock_movements_db if m['movement_type'] == 'transfer']
    return render_template('inventory/transfers.html', movements=transfer_movements)


@inventory_bp.route('/transfers/new')
def new_transfer():
    """Display form to create stock transfer."""
    return render_template('inventory/new_transfer.html', 
                         items=stock_items_db,
                         warehouses=warehouses_db)


@inventory_bp.route('/transfers', methods=['POST'])
def create_transfer():
    """Create a stock transfer between warehouses."""
    try:
        item_id = int(request.form.get('item_id'))
        from_warehouse = int(request.form.get('from_warehouse'))
        to_warehouse = int(request.form.get('to_warehouse'))
        quantity = int(request.form.get('quantity'))
        
        if from_warehouse == to_warehouse:
            flash('Cannot transfer to the same warehouse', 'danger')
            return redirect(url_for('inventory.new_transfer'))
        
        item = next((i for i in stock_items_db if i['id'] == item_id and i['warehouse_id'] == from_warehouse), None)
        
        if not item:
            flash('Item not found in source warehouse', 'danger')
            return redirect(url_for('inventory.new_transfer'))
        
        if item['quantity'] < quantity:
            flash('Insufficient stock for transfer', 'danger')
            return redirect(url_for('inventory.new_transfer'))
        
        # Decrease from source
        item['quantity'] -= quantity
        
        # Increase in destination
        dest_item = next((i for i in stock_items_db if i['product_id'] == item['product_id'] and i['warehouse_id'] == to_warehouse), None)
        if dest_item:
            dest_item['quantity'] += quantity
        else:
            new_dest_id = max([i['id'] for i in stock_items_db], default=0) + 1
            dest_item = {
                "id": new_dest_id,
                "warehouse_id": to_warehouse,
                "product_id": item['product_id'],
                "product_name": item['product_name'],
                "quantity": quantity,
                "unit": item['unit'],
                "reorder_level": item['reorder_level'],
                "last_updated": datetime.now().strftime('%Y-%m-%d')
            }
            stock_items_db.append(dest_item)
        
        movement = {
            "id": len(stock_movements_db) + 1,
            "item_id": item_id,
            "product_name": item['product_name'],
            "warehouse_id": from_warehouse,
            "to_warehouse_id": to_warehouse,
            "movement_type": "transfer",
            "quantity_change": -quantity,
            "old_quantity": item['quantity'] + quantity,
            "new_quantity": item['quantity'],
            "reason": f"Transfer to warehouse {to_warehouse}",
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        stock_movements_db.append(movement)
        
        flash(f'Transferred {quantity} units successfully!', 'success')
        return redirect(url_for('inventory.index'))
    
    except Exception as e:
        flash(f'Error creating transfer: {str(e)}', 'danger')
        return render_template('inventory/new_transfer.html'), 400


@inventory_bp.route('/reports/low-stock')
def low_stock_report():
    """Generate low stock report."""
    low_stock_items = [i for i in stock_items_db if i['quantity'] <= i['reorder_level']]
    return render_template('inventory/reports/low_stock.html', items=low_stock_items)


@inventory_bp.route('/reports/valuation')
def valuation_report():
    """Generate inventory valuation report."""
    # Would calculate total value in real implementation
    return render_template('inventory/reports/valuation.html', items=stock_items_db)


@inventory_bp.route('/api/list')
def api_list():
    """API endpoint to list inventory items."""
    return jsonify({
        'success': True,
        'data': stock_items_db,
        'count': len(stock_items_db)
    })


@inventory_bp.route('/api/<int:item_id>')
def api_show(item_id: int):
    """API endpoint to get inventory item details."""
    item = next((i for i in stock_items_db if i['id'] == item_id), None)
    
    if not item:
        return jsonify({'success': False, 'error': 'Item not found'}), 404
    
    return jsonify({'success': True, 'data': item})
