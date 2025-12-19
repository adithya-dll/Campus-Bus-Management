from flask import Blueprint, request, jsonify, session
from models.student import Student
from services.face_service import FaceService
from routes.auth import require_auth
from utils.validators import validate_required_fields, validate_email, sanitize_string
from config import Config
import logging

logger = logging.getLogger(__name__)

students_bp = Blueprint('students', __name__, url_prefix='/api/students')

@students_bp.route('/add', methods=['POST'])
@require_auth(['admin'])
def add_student():
    """Add a new student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('roll_number') or not data.get('name'):
            return jsonify({'error': 'Roll number and name are required'}), 400
        
        # Check if student already exists
        existing = Student.find_by_roll_number(data['roll_number'])
        if existing:
            return jsonify({'error': 'Student with this roll number already exists'}), 400
        
        # Validate email if provided
        if data.get('email') and not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Sanitize inputs
        data['name'] = sanitize_string(data['name'])
        
        # Create student
        student = Student.create(data)
        
        logger.info(f"Student created: {student['roll_number']}")
        
        return jsonify({
            'message': 'Student added successfully',
            'student': student
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding student: {str(e)}")
        return jsonify({'error': 'Failed to add student'}), 500


@students_bp.route('/update/<roll_number>', methods=['PUT'])
@require_auth(['admin'])
def update_student(roll_number):
    """Update student information"""
    try:
        data = request.get_json()
        
        # Check if student exists
        student = Student.find_by_roll_number(roll_number)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Validate email if provided
        if data.get('email') and not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Sanitize inputs
        if 'name' in data:
            data['name'] = sanitize_string(data['name'])
        
        # Update student
        success = Student.update(roll_number, data)
        
        if success:
            updated_student = Student.find_by_roll_number(roll_number)
            logger.info(f"Student updated: {roll_number}")
            return jsonify({
                'message': 'Student updated successfully',
                'student': updated_student
            }), 200
        else:
            return jsonify({'error': 'No changes made'}), 400
            
    except Exception as e:
        logger.error(f"Error updating student: {str(e)}")
        return jsonify({'error': 'Failed to update student'}), 500


@students_bp.route('/get/<roll_number>', methods=['GET'])
@require_auth()
def get_student(roll_number):
    """Get student by roll number"""
    try:
        student = Student.find_by_roll_number(roll_number)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Remove sensitive data for non-admin users
        if session.get('user_type') != 'admin':
            student.pop('face_encoding', None)
        
        return jsonify({'student': student}), 200
        
    except Exception as e:
        logger.error(f"Error getting student: {str(e)}")
        return jsonify({'error': 'Failed to get student'}), 500


@students_bp.route('/list', methods=['GET'])
@require_auth(['admin', 'driver'])
def list_students():
    """List all students with pagination"""
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 100))
        
        # Optional filters
        filters = {}
        if request.args.get('assigned_bus'):
            filters['assigned_bus'] = request.args.get('assigned_bus')
        if request.args.get('pass_valid') is not None:
            filters['bus_pass_valid'] = request.args.get('pass_valid').lower() == 'true'
        
        students = Student.find_all(filters, skip, limit)
        total = Student.count(filters)
        
        # Remove face encodings from list (too large)
        for student in students:
            student.pop('face_encoding', None)
        
        return jsonify({
            'students': students,
            'total': total,
            'skip': skip,
            'limit': limit
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing students: {str(e)}")
        return jsonify({'error': 'Failed to list students'}), 500


@students_bp.route('/delete/<roll_number>', methods=['DELETE'])
@require_auth(['admin'])
def delete_student(roll_number):
    """Delete a student"""
    try:
        success = Student.delete(roll_number)
        
        if success:
            logger.info(f"Student deleted: {roll_number}")
            return jsonify({'message': 'Student deleted successfully'}), 200
        else:
            return jsonify({'error': 'Student not found'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting student: {str(e)}")
        return jsonify({'error': 'Failed to delete student'}), 500


@students_bp.route('/register-face/<roll_number>', methods=['POST'])
@require_auth(['admin'])
def register_face(roll_number):
    """Register face for a student"""
    try:
        # Check if student exists
        student = Student.find_by_roll_number(roll_number)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Check if file is present
        if 'face_image' not in request.files:
            return jsonify({'error': 'No face image provided'}), 400
        
        file = request.files['face_image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file data
        image_data = file.read()
        
        # Encode face
        face_encoding, success, error_msg = FaceService.encode_face(image_data)
        
        if not success:
            return jsonify({'error': error_msg}), 400
        
        # Save image
        image_path = FaceService.save_face_image(image_data, roll_number)
        
        if not image_path:
            return jsonify({'error': 'Failed to save face image'}), 500
        
        # Update student with face encoding
        success = Student.update_face_encoding(roll_number, face_encoding, image_path)
        
        if success:
            logger.info(f"Face registered for student: {roll_number}")
            return jsonify({
                'message': 'Face registered successfully',
                'image_path': image_path
            }), 200
        else:
            return jsonify({'error': 'Failed to update student'}), 500
            
    except Exception as e:
        logger.error(f"Error registering face: {str(e)}")
        return jsonify({'error': f'Failed to register face: {str(e)}'}), 500
