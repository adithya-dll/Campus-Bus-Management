from flask import Blueprint, request, jsonify, session
from models.student import Student
from models.driver import Driver
from utils.validators import validate_required_fields
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
@validate_required_fields(['user_id', 'password', 'user_type'])
def login():
    """
    Login endpoint for students, drivers, and admins
    
    Request body:
        {
            "user_id": "string",
            "password": "string",
            "user_type": "student|driver|admin"
        }
    """
    try:
        data = request.get_json()
        user_id = data['user_id']
        password = data['password']
        user_type = data['user_type']
        
        if user_type not in ['student', 'driver', 'admin']:
            return jsonify({'error': 'Invalid user type'}), 400
        
        user = None
        
        if user_type == 'student':
            # For students, we check if student exists with the roll number
            user = Student.find_by_roll_number(user_id)
            # In production, store and verify hashed passwords
            if user and data.get('password'):  # Simplified check
                user['user_type'] = 'student'
            else:
                user = None
                
        elif user_type == 'driver':
            user = Driver.find_by_credentials(user_id, password)
            if user:
                user['user_type'] = 'driver'
                
        elif user_type == 'admin':
            # Hardcoded admin for demo (in production, use proper admin table)
            if user_id == 'admin' and password == 'admin123':
                user = {
                    'user_id': 'admin',
                    'name': 'Administrator',
                    'user_type': 'admin'
                }
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create session
        session['user_id'] = user_id
        session['user_type'] = user_type
        session.permanent = True
        
        # Remove password from response
        user.pop('password', None)
        
        logger.info(f"{user_type.capitalize()} logged in: {user_id}")
        
        return jsonify({
            'message': 'Login successful',
            'user': user
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout endpoint"""
    try:
        user_id = session.get('user_id')
        user_type = session.get('user_type')
        
        session.clear()
        
        logger.info(f"User logged out: {user_id} ({user_type})")
        
        return jsonify({'message': 'Logout successful'}), 200
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500


@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    try:
        if 'user_id' in session:
            return jsonify({
                'authenticated': True,
                'user_id': session['user_id'],
                'user_type': session['user_type']
            }), 200
        else:
            return jsonify({'authenticated': False}), 200
            
    except Exception as e:
        logger.error(f"Auth check error: {str(e)}")
        return jsonify({'error': 'Auth check failed'}), 500


def require_auth(allowed_types=None):
    """
    Decorator to require authentication
    
    Args:
        allowed_types: List of allowed user types (default: all)
    """
    from functools import wraps
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            if allowed_types and session.get('user_type') not in allowed_types:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return wrapper
    return decorator
