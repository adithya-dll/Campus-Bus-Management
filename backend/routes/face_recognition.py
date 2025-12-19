from flask import Blueprint, request, jsonify
from models.student import Student
from models.log import Log
from services.face_service import FaceService
from routes.auth import require_auth
from utils.validators import validate_required_fields, allowed_file
from config import Config
import logging

logger = logging.getLogger(__name__)

face_bp = Blueprint('face_recognition', __name__, url_prefix='/api/face')

@face_bp.route('/verify', methods=['POST'])
@require_auth(['driver'])
@validate_required_fields(['bus_id'])
def verify_face():
    """
    Verify a student face (called by driver app during entry)
    
    Expects:
        - bus_id: Bus ID
        - face_image: Image file with student face
    """
    try:
        from flask import session
        data = request.form  # Using form instead of JSON because of file upload
        bus_id = data.get('bus_id')
        driver_id = session.get('user_id')
        
        # Check if file is present
        if 'face_image' not in request.files:
            return jsonify({'error': 'No face image provided'}), 400
        
        file = request.files['face_image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file data
        image_data = file.read()
        
        # Encode the captured face
        captured_encoding, success, error_msg = FaceService.encode_face(image_data)
        
        if not success:
            # Create log for failed detection
            Log.create_entry_log({
                'bus_id': bus_id,
                'driver_id': driver_id,
                'status': 'invalid_no_face',
                'notes': error_msg
            })
            
            return jsonify({
                'verified': False,
                'reason': error_msg
            }), 200
        
        # Get all registered student face encodings
        known_encodings = Student.get_all_encodings()
        
        # Verify face
        result = FaceService.verify_face(captured_encoding, known_encodings)
        
        # Create entry log
        log_data = {
            'bus_id': bus_id,
            'driver_id': driver_id,
            'student_id': result.get('student_id'),
            'student_name': result.get('student_name'),
            'confidence': result.get('confidence'),
        }
        
        if result['matched'] and result['bus_pass_valid']:
            log_data['status'] = 'valid'
            Log.create_entry_log(log_data)
            
            logger.info(f"Face verified successfully: {result['student_id']} on bus {bus_id}")
            
            return jsonify({
                'verified': True,
                'student_id': result['student_id'],
                'student_name': result['student_name'],
                'confidence': result['confidence'],
                'message': result['message']
            }), 200
            
        elif result['matched'] and not result['bus_pass_valid']:
            log_data['status'] = 'invalid_pass'
            Log.create_entry_log(log_data)
            
            # Create alert
            Log.create_alert({
                'alert_type': 'invalid_entry',
                'severity': 'medium',
                'bus_id': bus_id,
                'driver_id': driver_id,
                'student_id': result['student_id'],
                'message': f"Student {result['student_id']} has invalid/expired bus pass"
            })
            
            logger.warning(f"Invalid pass: {result['student_id']} on bus {bus_id}")
            
            return jsonify({
                'verified': False,
                'student_id': result['student_id'],
                'student_name': result['student_name'],
                'reason': 'Bus pass is invalid or expired',
                'confidence': result['confidence']
            }), 200
            
        else:
            log_data['status'] = 'not_found'
            Log.create_entry_log(log_data)
            
            # Create alert
            Log.create_alert({
                'alert_type': 'invalid_entry',
                'severity': 'high',
                'bus_id': bus_id,
                'driver_id': driver_id,
                'message': 'Unrecognized person attempted entry'
            })
            
            logger.warning(f"Face not recognized on bus {bus_id}")
            
            return jsonify({
                'verified': False,
                'reason': 'Face not recognized',
                'message': result['message']
            }), 200
            
    except Exception as e:
        logger.error(f"Error during face verification: {str(e)}")
        return jsonify({'error': f'Verification failed: {str(e)}'}), 500


@face_bp.route('/detect', methods=['POST'])
@require_auth(['driver'])
def detect_faces():
    """
    Detect number of faces in a frame (for driver app to know when to capture)
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        image_data = file.read()
        
        # Detect faces
        face_count = FaceService.detect_faces_in_frame(image_data)
        
        return jsonify({
            'face_count': face_count
        }), 200
        
    except Exception as e:
        logger.error(f"Error detecting faces: {str(e)}")
        return jsonify({'error': 'Face detection failed'}), 500
