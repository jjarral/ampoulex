"""
Pytest configuration and fixtures for Ampoulex tests.
"""
import pytest
from app import create_app, db
from app.models import User, Product, Customer
from datetime import datetime


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key-for-testing-only'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def authenticated_client(client, app):
    """Create authenticated test client."""
    with app.app_context():
        # Create test user
        user = User(
            username='testuser',
            email='test@example.com',
            role='user',
            is_active=True
        )
        user.set_password('testpassword123')
        db.session.add(user)
        db.session.commit()
        
        # Login
        client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword123'
        }, follow_redirects=True)
        
        yield client
        
        # Cleanup
        db.session.delete(user)
        db.session.commit()


@pytest.fixture
def admin_client(client, app):
    """Create admin authenticated test client."""
    with app.app_context():
        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        # Login
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        
        yield client
        
        # Cleanup
        db.session.delete(admin)
        db.session.commit()


@pytest.fixture
def sample_product(app):
    """Create a sample product for testing."""
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
        
        yield product
        
        db.session.delete(product)
        db.session.commit()


@pytest.fixture
def sample_customer(app):
    """Create a sample customer for testing."""
    with app.app_context():
        customer = Customer(
            name='Test Customer',
            business_name='Test Business Inc.',
            email='customer@test.com',
            phone='1234567890',
            address='123 Test Street',
            payment_terms='cash',
            is_active=True,
            is_deleted=False
        )
        db.session.add(customer)
        db.session.commit()
        
        yield customer
        
        db.session.delete(customer)
        db.session.commit()
