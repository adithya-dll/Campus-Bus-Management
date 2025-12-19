import re
from functools import wraps
from flask import request, jsonify

def validate_required_fields(required_fields):
    """Decorator to validate required fields in request JSON"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                }), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_student_id(student_id):
    """Validate student ID format"""
    # Assuming format: alphanumeric, 3-20 characters
    return bool(re.match(r'^[a-zA-Z0-9]{3,20}$', student_id))

def validate_bus_id(bus_id):
    """Validate bus ID format"""
    return bool(re.match(r'^[a-zA-Z0-9-]{2,20}$', bus_id))

def validate_coordinates(lat, lng):
    """Validate GPS coordinates"""
    try:
        lat = float(lat)
        lng = float(lng)
        return -90 <= lat <= 90 and -180 <= lng <= 180
    except (ValueError, TypeError):
        return False

def sanitize_string(value, max_length=100):
    """Sanitize string input"""
    if not isinstance(value, str):
        return str(value)
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>\"\'%;()&+]', '', value)
    return sanitized[:max_length].strip()

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
