"""
Admin Blueprint Routes

Handles all admin-related HTTP requests including user management,
system settings, audit logs, and system configuration.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from typing import Dict, List, Any, Optional
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# In-memory storage (replace with database in production)
users_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@ampoulex.com",
        "role": "administrator",
        "status": "active",
        "last_login": "2024-03-16 09:30",
        "created_at": "2024-01-01"
    },
    {
        "id": 2,
        "username": "manager",
        "email": "manager@ampoulex.com",
        "role": "manager",
        "status": "active",
        "last_login": "2024-03-15 14:20",
        "created_at": "2024-01-15"
    },
    {
        "id": 3,
        "username": "operator",
        "email": "operator@ampoulex.com",
        "role": "operator",
        "status": "active",
        "last_login": "2024-03-16 08:00",
        "created_at": "2024-02-01"
    }
]

roles_db: List[Dict[str, Any]] = [
    {"id": 1, "name": "administrator", "permissions": ["all"]},
    {"id": 2, "name": "manager", "permissions": ["view", "edit", "approve"]},
    {"id": 3, "name": "operator", "permissions": ["view", "edit"]},
    {"id": 4, "name": "viewer", "permissions": ["view"]}
]

audit_logs_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "user": "admin",
        "action": "LOGIN",
        "resource": "System",
        "details": "User logged in",
        "ip_address": "192.168.1.100",
        "timestamp": "2024-03-16 09:30:00"
    },
    {
        "id": 2,
        "user": "manager",
        "action": "UPDATE",
        "resource": "Product",
        "details": "Updated product Paracetamol 500mg",
        "ip_address": "192.168.1.101",
        "timestamp": "2024-03-15 14:25:00"
    },
    {
        "id": 3,
        "user": "admin",
        "action": "CREATE",
        "resource": "User",
        "details": "Created new user operator",
        "ip_address": "192.168.1.100",
        "timestamp": "2024-03-14 11:00:00"
    }
]

system_settings = {
    "company_name": "Ampoulex Pharmaceuticals",
    "system_email": "noreply@ampoulex.com",
    "timezone": "UTC",
    "date_format": "YYYY-MM-DD",
    "currency": "USD",
    "maintenance_mode": False,
    "allow_registration": False,
    "session_timeout": 3600
}


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user') or session.get('role') != 'administrator':
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def index():
    """Admin dashboard."""
    stats = {
        "total_users": len(users_db),
        "active_users": len([u for u in users_db if u['status'] == 'active']),
        "total_roles": len(roles_db),
        "audit_entries": len(audit_logs_db),
        "recent_logins": len([l for l in audit_logs_db if l['action'] == 'LOGIN' and '2024-03-16' in l['timestamp']])
    }
    
    return render_template('admin/index.html', stats=stats, settings=system_settings)


@admin_bp.route('/users')
@admin_required
def users():
    """List all users."""
    role_filter = request.args.get('role', '')
    status_filter = request.args.get('status', '')
    
    filtered_users = users_db
    
    if role_filter:
        filtered_users = [u for u in filtered_users if u['role'] == role_filter]
    
    if status_filter:
        filtered_users = [u for u in filtered_users if u['status'] == status_filter]
    
    return render_template('admin/users.html', 
                         users=filtered_users,
                         roles=roles_db,
                         role_filter=role_filter,
                         status_filter=status_filter)


@admin_bp.route('/users/new')
@admin_required
def new_user():
    """Display form to create new user."""
    return render_template('admin/new_user.html', roles=roles_db)


@admin_bp.route('/users', methods=['POST'])
@admin_required
def create_user():
    """Create a new user."""
    try:
        new_id = max([u['id'] for u in users_db], default=0) + 1
        
        new_user = {
            "id": new_id,
            "username": request.form.get('username'),
            "email": request.form.get('email'),
            "role": request.form.get('role'),
            "status": "active",
            "last_login": None,
            "created_at": datetime.now().strftime('%Y-%m-%d')
        }
        
        users_db.append(new_user)
        
        # Log action
        audit_logs_db.insert(0, {
            "id": len(audit_logs_db) + 1,
            "user": session.get('user', 'system'),
            "action": "CREATE",
            "resource": "User",
            "details": f"Created new user {new_user['username']}",
            "ip_address": request.remote_addr,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        flash(f'User "{new_user["username"]}" created successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    except Exception as e:
        flash(f'Error creating user: {str(e)}', 'danger')
        return render_template('admin/new_user.html', roles=roles_db), 400


@admin_bp.route('/users/<int:user_id>')
@admin_required
def show_user(user_id: int):
    """Display user details."""
    user = next((u for u in users_db if u['id'] == user_id), None)
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    
    user_logs = [log for log in audit_logs_db if log['user'] == user['username']]
    
    return render_template('admin/show_user.html', user=user, logs=user_logs)


@admin_bp.route('/users/<int:user_id>/edit')
@admin_required
def edit_user(user_id: int):
    """Display form to edit user."""
    user = next((u for u in users_db if u['id'] == user_id), None)
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/edit_user.html', user=user, roles=roles_db)


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id: int):
    """Update user information."""
    try:
        user = next((u for u in users_db if u['id'] == user_id), None)
        
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('admin.users'))
        
        old_role = user['role']
        user['email'] = request.form.get('email')
        user['role'] = request.form.get('role')
        user['status'] = request.form.get('status')
        
        # Log action
        audit_logs_db.insert(0, {
            "id": len(audit_logs_db) + 1,
            "user": session.get('user', 'system'),
            "action": "UPDATE",
            "resource": "User",
            "details": f"Updated user {user['username']} (role: {old_role} -> {user['role']})",
            "ip_address": request.remote_addr,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        flash(f'User "{user["username"]}" updated successfully!', 'success')
        return redirect(url_for('admin.show_user', user_id=user_id))
    
    except Exception as e:
        flash(f'Error updating user: {str(e)}', 'danger')
        return render_template('admin/edit_user.html', user=user, roles=roles_db), 400


@admin_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
@admin_required
def deactivate_user(user_id: int):
    """Deactivate a user."""
    try:
        user = next((u for u in users_db if u['id'] == user_id), None)
        
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('admin.users'))
        
        if user['username'] == 'admin':
            flash('Cannot deactivate the main admin account', 'danger')
            return redirect(url_for('admin.users'))
        
        user['status'] = 'inactive'
        
        flash(f'User "{user["username"]}" deactivated!', 'warning')
        return redirect(url_for('admin.users'))
    
    except Exception as e:
        flash(f'Error deactivating user: {str(e)}', 'danger')
        return redirect(url_for('admin.users'))


@admin_bp.route('/roles')
@admin_required
def roles():
    """List all roles."""
    return render_template('admin/roles.html', roles=roles_db)


@admin_bp.route('/audit-logs')
@admin_required
def audit_logs():
    """View audit logs."""
    action_filter = request.args.get('action', '')
    user_filter = request.args.get('user', '')
    
    filtered_logs = audit_logs_db
    
    if action_filter:
        filtered_logs = [log for log in filtered_logs if log['action'] == action_filter]
    
    if user_filter:
        filtered_logs = [log for log in filtered_logs if log['user'] == user_filter]
    
    # Pagination (simple implementation)
    page = request.args.get('page', 1, type=int)
    per_page = 50
    start = (page - 1) * per_page
    end = start + per_page
    
    return render_template('admin/audit_logs.html', 
                         logs=filtered_logs[start:end],
                         total_logs=len(filtered_logs),
                         page=page,
                         per_page=per_page,
                         actions=["LOGIN", "LOGOUT", "CREATE", "UPDATE", "DELETE", "APPROVE", "REJECT"],
                         users=list(set([u['username'] for u in users_db])))


@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    """Manage system settings."""
    global system_settings
    
    if request.method == 'POST':
        try:
            system_settings['company_name'] = request.form.get('company_name')
            system_settings['system_email'] = request.form.get('system_email')
            system_settings['timezone'] = request.form.get('timezone')
            system_settings['date_format'] = request.form.get('date_format')
            system_settings['currency'] = request.form.get('currency')
            system_settings['maintenance_mode'] = request.form.get('maintenance_mode') == 'on'
            system_settings['allow_registration'] = request.form.get('allow_registration') == 'on'
            system_settings['session_timeout'] = int(request.form.get('session_timeout', 3600))
            
            flash('Settings updated successfully!', 'success')
            return redirect(url_for('admin.settings'))
        
        except Exception as e:
            flash(f'Error updating settings: {str(e)}', 'danger')
    
    return render_template('admin/settings.html', settings=system_settings)


@admin_bp.route('/system-info')
@admin_required
def system_info():
    """Display system information."""
    import sys
    import os
    
    info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "working_directory": os.getcwd(),
        "environment": os.getenv('FLASK_ENV', 'production'),
        "debug_mode": os.getenv('FLASK_DEBUG', 'False')
    }
    
    return render_template('admin/system_info.html', info=info)


@admin_bp.route('/api/users')
@admin_required
def api_users():
    """API endpoint to list users."""
    return jsonify({
        'success': True,
        'data': users_db,
        'count': len(users_db)
    })


@admin_bp.route('/api/logs')
@admin_required
def api_logs():
    """API endpoint to get audit logs."""
    return jsonify({
        'success': True,
        'data': audit_logs_db[:100],  # Last 100 entries
        'count': len(audit_logs_db)
    })
