"""
Tests for authentication and user management.
"""
import pytest
from app import db
from app.models import User


class TestAuthentication:
    """Test authentication functionality."""
    
    def test_login_page_loads(self, client):
        """Test that login page loads successfully."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_successful_login(self, client, app):
        """Test successful user login."""
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
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword123'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            assert b'Dashboard' in response.data or b'login' not in response.data.lower()
            
            # Cleanup
            db.session.delete(user)
            db.session.commit()
    
    def test_failed_login_wrong_password(self, client, app):
        """Test login with wrong password."""
        with app.app_context():
            # Create test user
            user = User(
                username='testuser',
                email='test@example.com',
                role='user',
                is_active=True
            )
            user.set_password('correctpassword')
            db.session.add(user)
            db.session.commit()
            
            # Try login with wrong password
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'wrongpassword'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            # Should show error message or stay on login page
            
            # Cleanup
            db.session.delete(user)
            db.session.commit()
    
    def test_logout(self, client, app):
        """Test user logout."""
        with app.app_context():
            # Create and login user
            user = User(
                username='testuser',
                email='test@example.com',
                role='user',
                is_active=True
            )
            user.set_password('testpassword123')
            db.session.add(user)
            db.session.commit()
            
            client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword123'
            })
            
            # Logout
            response = client.get('/logout', follow_redirects=True)
            assert response.status_code == 200
            
            # Cleanup
            db.session.delete(user)
            db.session.commit()
    
    def test_authenticated_user_redirected_from_login(self, authenticated_client):
        """Test that authenticated users are redirected from login page."""
        response = authenticated_client.get('/login', follow_redirects=False)
        # Should redirect to dashboard
        assert response.status_code in [301, 302, 303]


class TestUserModel:
    """Test User model functionality."""
    
    def test_create_user(self, app):
        """Test creating a new user."""
        with app.app_context():
            user = User(
                username='newuser',
                email='newuser@example.com',
                role='user',
                is_active=True
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            # Verify user was created
            saved_user = User.query.filter_by(username='newuser').first()
            assert saved_user is not None
            assert saved_user.email == 'newuser@example.com'
            assert saved_user.check_password('password123')
            
            # Cleanup
            db.session.delete(saved_user)
            db.session.commit()
    
    def test_user_password_hashing(self, app):
        """Test that passwords are properly hashed."""
        with app.app_context():
            user = User(
                username='hashuser',
                email='hashuser@example.com',
                is_active=True
            )
            user.set_password('mysecretpassword')
            
            # Add and commit to persist the user
            db.session.add(user)
            db.session.commit()
            
            # Password should be hashed
            assert user.password_hash != 'mysecretpassword'
            assert len(user.password_hash) > 20
            
            # Should verify correctly
            assert user.check_password('mysecretpassword')
            assert not user.check_password('wrongpassword')
            
            # Cleanup
            db.session.delete(user)
            db.session.commit()
    
    def test_user_failed_login_attempts(self, app):
        """Test failed login attempt tracking."""
        with app.app_context():
            user = User(
                username='lockuser',
                email='lockuser@example.com',
                is_active=True
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            # Simulate failed logins
            for i in range(5):
                user.record_failed_login()
            
            # User should be locked after 5 attempts
            assert user.is_locked()
            assert user.failed_login_attempts >= 5
            
            # Cleanup
            db.session.delete(user)
            db.session.commit()
    
    def test_user_role_default(self, app):
        """Test default user role."""
        with app.app_context():
            user = User(
                username='roleuser',
                email='roleuser@example.com',
                is_active=True
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            assert user.role == 'user'
            
            # Cleanup
            db.session.delete(user)
            db.session.commit()
