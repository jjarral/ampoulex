"""
Unit Tests for Product Service

Tests the business logic layer for product operations.
"""

import pytest
from unittest.mock import MagicMock, patch

from app.services.product_service import ProductService
from app.models import Product, BOMItem


class TestProductService:
    """Test cases for ProductService"""
    
    def test_get_all_products_no_filters(self):
        """Test getting all products without filters"""
        with patch('app.services.product_service.Product') as mock_product:
            # Setup mock
            mock_query = MagicMock()
            mock_product.query = mock_query
            mock_paginate = MagicMock()
            mock_paginate.items = []
            mock_paginate.page = 1
            mock_paginate.per_page = 20
            mock_paginate.total = 0
            mock_paginate.pages = 0
            mock_paginate.has_next = False
            mock_paginate.has_prev = False
            mock_query.filter_by.return_value.order_by.return_value.paginate.return_value = mock_paginate
            
            # Call service
            result = ProductService.get_all_products()
            
            # Assertions
            assert 'products' in result
            assert 'pagination' in result
            assert result['pagination']['page'] == 1
            mock_query.filter_by.assert_called_once_with(is_deleted=False)
    
    def test_get_all_products_with_search(self):
        """Test getting products with search filter"""
        with patch('app.services.product_service.Product') as mock_product:
            # Setup mock
            mock_query = MagicMock()
            mock_product.query = mock_query
            mock_filter_result = MagicMock()
            mock_paginate = MagicMock()
            mock_paginate.items = []
            mock_paginate.page = 1
            mock_paginate.per_page = 20
            mock_paginate.total = 0
            mock_paginate.pages = 0
            mock_paginate.has_next = False
            mock_paginate.has_prev = False
            
            mock_query.filter_by.return_value.filter.return_value.order_by.return_value.paginate.return_value = mock_paginate
            
            # Call service
            result = ProductService.get_all_products(search='test')
            
            # Assertions
            assert 'products' in result
            mock_query.filter_by.assert_called_once_with(is_deleted=False)
    
    def test_create_product(self):
        """Test creating a new product"""
        with patch('app.services.product_service.db') as mock_db:
            # Setup mock
            mock_session = MagicMock()
            mock_db.session = mock_session
            
            # Test data
            product_data = {
                'name': 'Test Product',
                'sku': 'TEST-001',
                'base_price': 100.0,
                'stock': 50
            }
            
            # Call service
            result = ProductService.create_product(product_data)
            
            # Assertions
            assert isinstance(result, Product)
            assert result.name == 'Test Product'
            assert result.sku == 'TEST-001'
            assert result.base_price == 100.0
            assert result.stock == 50
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
    
    def test_update_product_success(self):
        """Test updating an existing product"""
        with patch('app.services.product_service.Product') as mock_product:
            # Setup mock
            mock_instance = MagicMock()
            mock_instance.id = 1
            mock_instance.name = 'Old Name'
            mock_product.query.get.return_value = mock_instance
            
            # Update data
            update_data = {
                'name': 'New Name',
                'base_price': 150.0
            }
            
            # Call service
            result = ProductService.update_product(1, update_data)
            
            # Assertions
            assert result is not None
            assert result.name == 'New Name'
            assert result.base_price == 150.0
    
    def test_update_product_not_found(self):
        """Test updating a non-existent product"""
        with patch('app.services.product_service.Product') as mock_product:
            # Setup mock
            mock_product.query.get.return_value = None
            
            # Call service
            result = ProductService.update_product(999, {'name': 'Test'})
            
            # Assertions
            assert result is None
    
    def test_delete_product_success(self):
        """Test soft deleting a product"""
        with patch('app.services.product_service.Product') as mock_product:
            # Setup mock
            mock_instance = MagicMock()
            mock_product.query.get.return_value = mock_instance
            
            # Call service
            result = ProductService.delete_product(1)
            
            # Assertions
            assert result is True
            assert mock_instance.is_deleted is True
    
    def test_delete_product_not_found(self):
        """Test deleting a non-existent product"""
        with patch('app.services.product_service.Product') as mock_product:
            # Setup mock
            mock_product.query.get.return_value = None
            
            # Call service
            result = ProductService.delete_product(999)
            
            # Assertions
            assert result is False
    
    def test_check_low_stock(self):
        """Test checking for low stock products"""
        with patch('app.services.product_service.Product') as mock_product_class:
            # Setup mock to support comparison operations
            mock_stock_column = MagicMock()
            mock_stock_column.__lt__ = MagicMock(return_value='stock_lt_mock')
            mock_product_class.stock = mock_stock_column
            
            mock_is_deleted = MagicMock()
            mock_is_deleted.__eq__ = MagicMock(return_value='is_deleted_eq_mock')
            mock_product_class.is_deleted = mock_is_deleted
            
            mock_query = MagicMock()
            mock_product_class.query = mock_query
            
            mock_filter_result = MagicMock()
            mock_query.filter.return_value = mock_filter_result
            mock_filter_result.all.return_value = []
            
            # Call service
            result = ProductService.check_low_stock(threshold=100)
            
            # Assertions
            assert isinstance(result, list)
            mock_query.filter.assert_called_once()


class TestProductServiceBOM:
    """Test cases for BOM-related operations"""
    
    def test_get_bom_items(self):
        """Test getting BOM items for a product"""
        with patch('app.services.product_service.BOMItem') as mock_bom_item:
            # Setup mock
            mock_query = MagicMock()
            mock_bom_item.query = mock_query
            mock_filter = MagicMock()
            mock_bom_items = []
            mock_filter.all.return_value = mock_bom_items
            mock_query.filter_by.return_value = mock_filter
            
            # Call service
            result = ProductService.get_bom_items(1)
            
            # Assertions
            assert isinstance(result, list)
            mock_query.filter_by.assert_called_once_with(
                product_id=1,
                is_active=True
            )
    
    def test_update_bom(self):
        """Test updating BOM items"""
        with patch('app.services.product_service.BOMItem') as mock_bom_item:
            with patch('app.services.product_service.db') as mock_db:
                # Setup mocks
                mock_query = MagicMock()
                mock_bom_item.query = mock_query
                mock_session = MagicMock()
                mock_db.session = mock_session
                
                # Test data
                bom_items = [
                    {'raw_material_id': 1, 'quantity_required': 10},
                    {'raw_material_id': 2, 'quantity_required': 20}
                ]
                
                # Call service
                result = ProductService.update_bom(1, bom_items)
                
                # Assertions
                assert result is True
                mock_query.filter_by.assert_called_once_with(product_id=1)
                mock_query.filter_by.return_value.delete.assert_called_once()
                assert mock_session.add.call_count == 2
                mock_session.commit.assert_called_once()
