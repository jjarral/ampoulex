"""
Authentication Blueprint

Handles user authentication, login, logout, and password management.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Please provide both username and password.', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            flash('Invalid username or password.', 'error')
            return render_template('auth/login.html')
        
        # Check if account is locked
        if user.is_locked():
            flash('Account is temporarily locked. Please try again later.', 'error')
            return render_template('auth/login.html')
        
        if not user.check_password(password):
            user.record_failed_login()
            db.session.commit()
            
            if user.is_locked():
                flash(f'Account locked due to multiple failed attempts. Try again after 15 minutes.', 'error')
            else:
                flash('Invalid username or password.', 'error')
            return render_template('auth/login.html')
        
        # Successful login
        user.record_successful_login()
        db.session.commit()
        
        login_user(user, remember=remember)
        
        # Store session info
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        
        flash(f'Welcome back, {user.username}!', 'success')
        
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    
    # Clear session data
    session.clear()
    
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Handle password change"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html')
        
        if len(new_password) < 8:
            flash('New password must be at least 8 characters long.', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return render_template('auth/change_password.html')
        
        current_user.set_password(new_password)
        current_user.must_change_password = False
        db.session.commit()
        
        flash('Password changed successfully.', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/change_password.html')
