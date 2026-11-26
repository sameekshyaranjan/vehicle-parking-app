from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ..models.user import User
def admin_required(f):
    """Decorator to require admin role for access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return jsonify({
                'error': True,
                'message': 'Admin access required'
            }), 403
            
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    """Decorator to require authenticated user"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({
                'error': True,
                'message': 'Valid user required'
            }), 401
        return f(*args, **kwargs)
    return decorated_function
def success_response(data=None, message="Success", status_code=200):
    """Standard success response format"""
    response = {
        'error': False,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def error_response(message="An error occurred", status_code=400, details=None):
    """Standard error response format"""
    response = {
        'error': True,
        'message': message
    }
    if details:
        response['details'] = details
    return jsonify(response), status_code