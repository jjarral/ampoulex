"""Payroll Blueprint"""
from flask import Blueprint, jsonify

payroll_bp = Blueprint('payroll', __name__, url_prefix='/payroll')

@payroll_bp.route('/')
def index():
    """List all payroll"""
    return jsonify({'message': 'Payroll module', 'status': 'placeholder'})
