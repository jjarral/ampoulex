"""
Tests for product management.
"""
import pytest
from app import db
from app.models import Product


class TestProductModel:
    """Test Product model functionality."""
    
    def test_create_product(self, app):
        """Test creating a new product."""
        with app.app_context():
            product = Product(
                name='Test Product - Clear',
                product_type='Ampoule',
                specification='10ml',
                base_name='Test Product',
                volume_cc=10.0,
                glass_type='Type I',
                neck_finish='13mm',
                sku='TEST-001',
                color='Clear',
                stock=10000,
                base_price=100,
                is_active=True,
                is_deleted=False
            )
            db.session.add(product)
            db.session.commit()
            
            # Verify product was created
            saved_product = Product.query.filter_by(sku='TEST-001').first()
            assert saved_product is not None
            assert saved_product.name == 'Test Product - Clear'
            assert saved_product.volume_cc == 10.0
            assert saved_product.stock == 10000
            
            # Cleanup
            db.session.delete(saved_product)
            db.session.commit()
    
    def test_product_default_values(self, app):
        """Test product default values."""
        with app.app_context():
            product = Product(
                name='Minimal Product',
                is_active=True
            )
            db.session.add(product)
            db.session.commit()
            
            # Check defaults
            assert product.is_deleted == False
            assert product.stock == 0
            assert product.base_price == 0 or product.base_price is None
            
            # Cleanup
            db.session.delete(product)
            db.session.commit()
    
    def test_product_soft_delete(self, sample_product):
        """Test soft delete functionality."""
        # Soft delete
        sample_product.is_deleted = True
        db.session.commit()
        
        # Should be marked as deleted
        assert sample_product.is_deleted == True
        
        # Query should exclude deleted by filter
        active_products = Product.query.filter_by(is_deleted=False).all()
        assert sample_product not in active_products
    
    def test_product_stock_adjustment(self, sample_product):
        """Test product stock adjustment."""
        initial_stock = sample_product.stock
        
        # Increase stock
        sample_product.stock += 5000
        db.session.commit()
        
        assert sample_product.stock == initial_stock + 5000
        
        # Decrease stock
        sample_product.stock -= 2000
        db.session.commit()
        
        assert sample_product.stock == initial_stock + 3000
    
    def test_product_search_by_name(self, app, sample_product):
        """Test searching products by name."""
        with app.app_context():
            # Create another product
            product2 = Product(
                name='Another Product - Blue',
                product_type='Ampoule',
                color='Blue',
                is_active=True,
                is_deleted=False
            )
            db.session.add(product2)
            db.session.commit()
            
            # Search
            results = Product.query.filter(
                Product.name.ilike('%Product%'),
                Product.is_deleted == False
            ).all()
            
            assert len(results) >= 2
            
            # Cleanup
            db.session.delete(product2)
            db.session.commit()


class TestProductRoutes:
    """Test product route handlers."""
    
    def test_products_page_requires_login(self, client):
        """Test that products page requires authentication."""
        response = client.get('/products', follow_redirects=False)
        assert response.status_code in [301, 302, 303]
        assert '/login' in response.location
    
    def test_add_product_page_requires_login(self, client):
        """Test that add product page requires authentication."""
        response = client.get('/products/add', follow_redirects=False)
        assert response.status_code in [301, 302, 303]
    
    def test_products_page_loads_for_authenticated_user(self, authenticated_client):
        """Test that products page loads for authenticated users."""
        response = authenticated_client.get('/products')
        assert response.status_code == 200
