"""
Services Package

Business logic layer separated from routes for better testability and maintainability.
"""

from app.services.product_service import ProductService
# from app.services.order_service import OrderService
# from app.services.customer_service import CustomerService

__all__ = [
    'ProductService',
    # 'OrderService',
    # 'CustomerService',
]
