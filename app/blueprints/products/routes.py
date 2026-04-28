"""Products Blueprint Module"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from sqlalchemy import func

from app import db
from app.models import Product, BOMItem, RawMaterial
from app.utils import log_activity

products_bp = Blueprint('products', __name__, url_prefix='/products')


@products_bp.route('/')
@login_required
def index():
    """List all products"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    product_type = request.args.get('type', '')
    
    query = Product.query.filter_by(is_deleted=False)
    
    if search:
        query = query.filter(
            (Product.name.ilike(f'%{search}%')) |
            (Product.sku.ilike(f'%{search}%'))
        )
    
    if product_type:
        query = query.filter_by(product_type=product_type)
    
    products = query.order_by(Product.name).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('products/index.html', 
                         products=products,
                         search=search,
                         product_type=product_type)


@products_bp.route('/new', methods=['GET', 'POST'])
@login_required
def add_product():
    """Add a new product"""
    if request.method == 'POST':
        try:
            product = Product(
                name=request.form.get('name', '').strip(),
                product_type=request.form.get('product_type', ''),
                specification=request.form.get('specification', ''),
                base_name=request.form.get('base_name', ''),
                volume_cc=float(request.form.get('volume_cc', 0) or 0),
                glass_type=request.form.get('glass_type', ''),
                neck_finish=request.form.get('neck_finish', ''),
                sku=request.form.get('sku', '').strip(),
                color=request.form.get('color', ''),
                stock=int(request.form.get('stock', 0) or 0),
                base_price=float(request.form.get('base_price', 0) or 0),
                price_per_unit=float(request.form.get('price_per_unit', 0) or 0),
                body_diameter=float(request.form.get('body_diameter', 0) or 0),
                overall_length=float(request.form.get('overall_length', 0) or 0),
                sealing_point=float(request.form.get('sealing_point', 0) or 0),
                body_length=float(request.form.get('body_length', 0) or 0),
                stem_diameter=float(request.form.get('stem_diameter', 0) or 0),
                wall_thickness=float(request.form.get('wall_thickness', 0) or 0),
                material_type=request.form.get('material_type', ''),
                usp_type=request.form.get('usp_type', ''),
                shape_type=request.form.get('shape_type', ''),
                dimensions=request.form.get('dimensions', ''),
                use_case=request.form.get('use_case', ''),
                paint_color=request.form.get('paint_color', ''),
                paint_type=request.form.get('paint_type', ''),
                printing_method=request.form.get('printing_method', ''),
                is_active=True
            )
            
            db.session.add(product)
            db.session.commit()
            
            log_activity('product_create', f'Created product: {product.name}')
            
            flash('Product created successfully.', 'success')
            return redirect(url_for('products.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating product: {str(e)}', 'error')
    
    return render_template('products/form.html', product=None)


@products_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """Edit an existing product"""
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            product.name = request.form.get('name', '').strip()
            product.product_type = request.form.get('product_type', '')
            product.specification = request.form.get('specification', '')
            product.base_name = request.form.get('base_name', '')
            product.volume_cc = float(request.form.get('volume_cc', 0) or 0)
            product.glass_type = request.form.get('glass_type', '')
            product.neck_finish = request.form.get('neck_finish', '')
            product.sku = request.form.get('sku', '').strip()
            product.color = request.form.get('color', '')
            product.stock = int(request.form.get('stock', 0) or 0)
            product.base_price = float(request.form.get('base_price', 0) or 0)
            product.price_per_unit = float(request.form.get('price_per_unit', 0) or 0)
            product.body_diameter = float(request.form.get('body_diameter', 0) or 0)
            product.overall_length = float(request.form.get('overall_length', 0) or 0)
            product.sealing_point = float(request.form.get('sealing_point', 0) or 0)
            product.body_length = float(request.form.get('body_length', 0) or 0)
            product.stem_diameter = float(request.form.get('stem_diameter', 0) or 0)
            product.wall_thickness = float(request.form.get('wall_thickness', 0) or 0)
            product.material_type = request.form.get('material_type', '')
            product.usp_type = request.form.get('usp_type', '')
            product.shape_type = request.form.get('shape_type', '')
            product.dimensions = request.form.get('dimensions', '')
            product.use_case = request.form.get('use_case', '')
            product.paint_color = request.form.get('paint_color', '')
            product.paint_type = request.form.get('paint_type', '')
            product.printing_method = request.form.get('printing_method', '')
            
            db.session.commit()
            
            log_activity('product_update', f'Updated product: {product.name}')
            
            flash('Product updated successfully.', 'success')
            return redirect(url_for('products.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {str(e)}', 'error')
    
    return render_template('products/form.html', product=product)


@products_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    """Soft delete a product"""
    product = Product.query.get_or_404(id)
    
    try:
        product.is_deleted = True
        db.session.commit()
        
        log_activity('product_delete', f'Deleted product: {product.name}')
        
        flash('Product deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'error')
    
    return redirect(url_for('products.index'))


@products_bp.route('/<int:id>/bom', methods=['GET', 'POST'])
@login_required
def manage_bom(id):
    """Manage Bill of Materials for a product"""
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Clear existing BOM items
            BOMItem.query.filter_by(product_id=id).delete()
            
            # Add new BOM items
            raw_material_ids = request.form.getlist('raw_material_id[]')
            quantities = request.form.getlist('quantity[]')
            
            for rm_id, qty in zip(raw_material_ids, quantities):
                if rm_id and qty:
                    bom_item = BOMItem(
                        product_id=id,
                        raw_material_id=int(rm_id),
                        quantity_required=float(qty),
                        is_active=True
                    )
                    db.session.add(bom_item)
            
            db.session.commit()
            
            log_activity('bom_update', f'Updated BOM for product: {product.name}')
            
            flash('BOM updated successfully.', 'success')
            return redirect(url_for('products.manage_bom', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating BOM: {str(e)}', 'error')
    
    bom_items = BOMItem.query.filter_by(product_id=id, is_active=True).all()
    raw_materials = RawMaterial.query.filter_by(is_active=True).all()
    
    return render_template('products/bom.html', 
                         product=product,
                         bom_items=bom_items,
                         raw_materials=raw_materials)


@products_bp.route('/<int:id>/labels')
@login_required
def generate_labels(id):
    """Generate product labels"""
    product = Product.query.get_or_404(id)
    return render_template('products/labels.html', product=product)


@products_bp.route('/api/list')
@login_required
def api_list():
    """API endpoint to list products"""
    products = Product.query.filter_by(is_deleted=False).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'sku': p.sku,
        'stock': p.stock,
        'price': float(p.base_price) if p.base_price else 0
    } for p in products])
