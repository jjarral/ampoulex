"""
Product Service

Handles all business logic related to products.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from app import db
from app.models import Product, BOMItem, RawMaterial


class ProductService:
    """Service class for product-related operations"""
    
    @staticmethod
    def get_all_products(
        page: int = 1,
        per_page: int = 20,
        search: str = '',
        product_type: str = '',
        include_deleted: bool = False
    ) -> Dict[str, Any]:
        """
        Get paginated list of products with optional filtering
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            search: Search term for name or SKU
            product_type: Filter by product type
            include_deleted: Whether to include deleted products
            
        Returns:
            Dictionary with products and pagination info
        """
        query = Product.query
        
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        
        if search:
            query = query.filter(
                (Product.name.ilike(f'%{search}%')) |
                (Product.sku.ilike(f'%{search}%'))
            )
        
        if product_type:
            query = query.filter_by(product_type=product_type)
        
        pagination = query.order_by(Product.name).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'products': pagination.items,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
    
    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[Product]:
        """Get a single product by ID"""
        return Product.query.get(product_id)
    
    @staticmethod
    def create_product(data: Dict[str, Any]) -> Product:
        """
        Create a new product
        
        Args:
            data: Dictionary containing product data
            
        Returns:
            Created Product instance
        """
        product = Product(
            name=data.get('name', '').strip(),
            product_type=data.get('product_type', ''),
            specification=data.get('specification', ''),
            base_name=data.get('base_name', ''),
            volume_cc=float(data.get('volume_cc', 0) or 0),
            glass_type=data.get('glass_type', ''),
            neck_finish=data.get('neck_finish', ''),
            sku=data.get('sku', '').strip(),
            color=data.get('color', ''),
            stock=int(data.get('stock', 0) or 0),
            base_price=float(data.get('base_price', 0) or 0),
            price_per_unit=float(data.get('price_per_unit', 0) or 0),
            body_diameter=float(data.get('body_diameter', 0) or 0),
            overall_length=float(data.get('overall_length', 0) or 0),
            sealing_point=float(data.get('sealing_point', 0) or 0),
            body_length=float(data.get('body_length', 0) or 0),
            stem_diameter=float(data.get('stem_diameter', 0) or 0),
            wall_thickness=float(data.get('wall_thickness', 0) or 0),
            material_type=data.get('material_type', ''),
            usp_type=data.get('usp_type', ''),
            shape_type=data.get('shape_type', ''),
            dimensions=data.get('dimensions', ''),
            use_case=data.get('use_case', ''),
            paint_color=data.get('paint_color', ''),
            paint_type=data.get('paint_type', ''),
            printing_method=data.get('printing_method', ''),
            is_active=True
        )
        
        db.session.add(product)
        db.session.commit()
        
        return product
    
    @staticmethod
    def update_product(product_id: int, data: Dict[str, Any]) -> Optional[Product]:
        """
        Update an existing product
        
        Args:
            product_id: ID of product to update
            data: Dictionary containing updated product data
            
        Returns:
            Updated Product instance or None if not found
        """
        product = Product.query.get(product_id)
        if not product:
            return None
        
        # Update fields
        for field in [
            'name', 'product_type', 'specification', 'base_name',
            'glass_type', 'neck_finish', 'sku', 'color',
            'material_type', 'usp_type', 'shape_type',
            'dimensions', 'use_case', 'paint_color',
            'paint_type', 'printing_method'
        ]:
            if field in data:
                setattr(product, field, data[field].strip() if isinstance(data[field], str) else data[field])
        
        # Update numeric fields
        numeric_fields = [
            'volume_cc', 'stock', 'base_price', 'price_per_unit',
            'body_diameter', 'overall_length', 'sealing_point',
            'body_length', 'stem_diameter', 'wall_thickness'
        ]
        
        for field in numeric_fields:
            if field in data:
                value = data[field]
                if isinstance(value, str):
                    value = float(value) if '.' in value else int(value)
                setattr(product, field, value or 0)
        
        db.session.commit()
        return product
    
    @staticmethod
    def delete_product(product_id: int) -> bool:
        """
        Soft delete a product
        
        Args:
            product_id: ID of product to delete
            
        Returns:
            True if successful, False if product not found
        """
        product = Product.query.get(product_id)
        if not product:
            return False
        
        product.is_deleted = True
        db.session.commit()
        return True
    
    @staticmethod
    def get_bom_items(product_id: int) -> List[BOMItem]:
        """Get all BOM items for a product"""
        return BOMItem.query.filter_by(
            product_id=product_id,
            is_active=True
        ).all()
    
    @staticmethod
    def update_bom(product_id: int, bom_items: List[Dict[str, Any]]) -> bool:
        """
        Update BOM items for a product
        
        Args:
            product_id: ID of product
            bom_items: List of dictionaries with raw_material_id and quantity_required
            
        Returns:
            True if successful
        """
        # Clear existing BOM items
        BOMItem.query.filter_by(product_id=product_id).delete()
        
        # Add new BOM items
        for item in bom_items:
            bom_item = BOMItem(
                product_id=product_id,
                raw_material_id=item['raw_material_id'],
                quantity_required=float(item['quantity_required']),
                is_active=True
            )
            db.session.add(bom_item)
        
        db.session.commit()
        return True
    
    @staticmethod
    def check_low_stock(threshold: int = 10000) -> List[Product]:
        """Get products with stock below threshold"""
        return Product.query.filter(
            Product.stock < threshold,
            Product.is_deleted == False
        ).all()
    
    @staticmethod
    def get_products_by_base_name(base_name: str) -> List[Product]:
        """Get all product variants with the same base name"""
        return Product.query.filter(
            Product.base_name == base_name,
            Product.is_deleted == False
        ).all()
