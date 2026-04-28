"""
Ampoulex Utilities Module

Common utility functions used across the application.
"""

import logging
from datetime import datetime
from functools import wraps
from flask import session, request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def log_activity(description: str, user_id: int = None) -> None:
    """
    Log a user activity for audit trail.
    
    Args:
        description: Description of the activity
        user_id: ID of the user performing the action (defaults to current user)
    
    TODO: Implement database storage for activity logs
    Currently logs to console/logger only
    """
    if user_id is None:
        # Try to get from session if available
        user_id = session.get('user_id', 'unknown')
    
    timestamp = datetime.utcnow().isoformat()
    log_message = f"[ACTIVITY] {timestamp} - User {user_id}: {description}"
    
    logger.info(log_message)
    
    # TODO: Save to database
    # ActivityLog(
    #     user_id=user_id,
    #     description=description,
    #     timestamp=datetime.utcnow(),
    #     ip_address=request.remote_addr
    # ).save()


def generate_reference_number(prefix: str, number: int) -> str:
    """
    Generate a formatted reference number.
    
    Args:
        prefix: Prefix for the reference (e.g., 'PO', 'SO', 'INV')
        number: Sequential number
    
    Returns:
        Formatted reference string (e.g., 'PO-2024-00001')
    """
    year = datetime.utcnow().year
    return f"{prefix}-{year}-{number:05d}"


def format_currency(amount: float, currency: str = 'USD') -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: Numeric amount
        currency: Currency code
    
    Returns:
        Formatted currency string
    """
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'EGP': 'E£'
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def parse_decimal(value) -> float:
    """
    Safely parse a value to decimal/float.
    
    Args:
        value: Value to parse (string, int, float, etc.)
    
    Returns:
        Float value or 0.0 if parsing fails
    """
    if value is None:
        return 0.0
    
    try:
        if isinstance(value, (int, float)):
            return float(value)
        
        # Remove currency symbols and commas
        cleaned = str(value).replace(',', '').replace('$', '').replace('€', '').replace('£', '')
        return float(cleaned)
    except (ValueError, TypeError):
        return 0.0


def validate_email(email: str) -> bool:
    """
    Basic email validation.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid email format, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        text: Input text to sanitize
    
    Returns:
        Sanitized text
    """
    if not text:
        return ''
    
    # Basic HTML entity encoding
    replacements = {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
        '"': '&quot;',
        "'": '&#x27;'
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text


__all__ = [
    'log_activity',
    'generate_reference_number',
    'format_currency',
    'parse_decimal',
    'validate_email',
    'sanitize_input',
    'logger'
]