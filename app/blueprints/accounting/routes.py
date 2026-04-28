"""Accounting Blueprint"""
from flask import Blueprint, jsonify

accounting_bp = Blueprint('accounting', __name__, url_prefix='/accounting')

@accounting_bp.route('/')
def index():
    """List all accounting"""
    return jsonify({'message': 'Accounting module', 'status': 'placeholder'})
