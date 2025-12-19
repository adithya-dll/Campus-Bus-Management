try:
    import face_recognition
    import numpy as np
    import cv2
    from PIL import Image
    import io
    import os
    from config import Config
    import logging
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    import logging


logger = logging.getLogger(__name__)

class FaceService:
    """Face recognition service using face_recognition library"""
    
    @staticmethod
    def encode_face(image_data):
        """
        Encode a face from image data
        
        Args:
            image_data: Binary image data or file path
            
        Returns:
            tuple: (face_encoding, success, error_message)
        """
        if not FACE_RECOGNITION_AVAILABLE:
            return None, False, "Face recognition library not installed. Install CMake and run: pip install face-recognition"
        
        try:
            # Load image
            if isinstance(image_data, str):
                # File path
                image = face_recognition.load_image_file(image_data)
            else:
                # Binary data
                pil_image = Image.open(io.BytesIO(image_data))
                image = np.array(pil_image)
            
            # Find faces in image
            face_locations = face_recognition.face_locations(
                image, 
                model=Config.FACE_RECOGNITION_MODEL
            )
            
            if len(face_locations) == 0:
                return None, False, "No face detected in image"
            
            if len(face_locations) > 1:
                logger.warning(f"Multiple faces detected ({len(face_locations)}), using the first one")
            
            # Encode the first face
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if len(face_encodings) == 0:
                return None, False, "Could not encode face"
            
            # Convert to list for JSON serialization
            encoding = face_encodings[0].tolist()
            
            return encoding, True, None
            
        except Exception as e:
            logger.error(f"Error encoding face: {str(e)}")
            return None, False, f"Error processing image: {str(e)}"
    
    @staticmethod
    def verify_face(captured_encoding, known_encodings_data, tolerance=None):
        """
        Verify a captured face against known face encodings
        
        Args:
            captured_encoding: Face encoding from captured image
            known_encodings_data: List of dicts with 'student_id', 'name', 'face_encoding', 'bus_pass_valid'
            tolerance: Match tolerance (lower is stricter), defaults to config value
            
        Returns:
            dict: {
                'matched': bool,
                'student_id': str or None,
                'student_name': str or None,
                'confidence': float,
                'bus_pass_valid': bool,
                'message': str
            }
        """
        if not FACE_RECOGNITION_AVAILABLE:
            return {
                'matched': False,
                'student_id': None,
                'student_name': None,
                'confidence': 0.0,
                'bus_pass_valid': False,
                'message': 'Face recognition library not installed'
            }
        
        if tolerance is None:
            tolerance = Config.FACE_RECOGNITION_TOLERANCE
        
        try:
            # Convert captured encoding to numpy array
            captured_array = np.array(captured_encoding)
            
            if len(known_encodings_data) == 0:
                return {
                    'matched': False,
                    'student_id': None,
                    'student_name': None,
                    'confidence': 0.0,
                    'bus_pass_valid': False,
                    'message': 'No registered students in database'
                }
            
            # Extract encodings and IDs
            known_encodings = []
            student_info = []
            
            for data in known_encodings_data:
                if data.get('face_encoding'):
                    known_encodings.append(np.array(data['face_encoding']))
                    student_info.append({
                        'student_id': data['student_id'],
                        'name': data.get('name', 'Unknown'),
                        'bus_pass_valid': data.get('bus_pass_valid', False)
                    })
            
            if len(known_encodings) == 0:
                return {
                    'matched': False,
                    'student_id': None,
                    'student_name': None,
                    'confidence': 0.0,
                    'bus_pass_valid': False,
                    'message': 'No valid face encodings found'
                }
            
            # Compare faces
            matches = face_recognition.compare_faces(
                known_encodings, 
                captured_array, 
                tolerance=tolerance
            )
            
            # Calculate face distances (lower is better match)
            face_distances = face_recognition.face_distance(known_encodings, captured_array)
            
            # Find best match
            if True in matches:
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    student = student_info[best_match_index]
                    confidence = 1 - face_distances[best_match_index]  # Convert distance to confidence
                    
                    # Check bus pass validity
                    if not student['bus_pass_valid']:
                        return {
                            'matched': True,
                            'student_id': student['student_id'],
                            'student_name': student['name'],
                            'confidence': float(confidence),
                            'bus_pass_valid': False,
                            'message': 'Student identified but bus pass is invalid or expired'
                        }
                    
                    return {
                        'matched': True,
                        'student_id': student['student_id'],
                        'student_name': student['name'],
                        'confidence': float(confidence),
                        'bus_pass_valid': True,
                        'message': 'Student verified successfully'
                    }
            
            # No match found
            return {
                'matched': False,
                'student_id': None,
                'student_name': None,
                'confidence': 0.0,
                'bus_pass_valid': False,
                'message': 'Face not recognized'
            }
            
        except Exception as e:
            logger.error(f"Error verifying face: {str(e)}")
            return {
                'matched': False,
                'student_id': None,
                'student_name': None,
                'confidence': 0.0,
                'bus_pass_valid': False,
                'message': f'Error during verification: {str(e)}'
            }
    
    @staticmethod
    def save_face_image(image_data, student_id):
        """
        Save face image to disk
        
        Args:
            image_data: Binary image data
            student_id: Student ID for filename
            
        Returns:
            str: File path if successful, None otherwise
        """
        try:
            # Create upload folder if it doesn't exist
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            
            # Generate filename
            filename = f"{student_id}_{int(datetime.now().timestamp())}.jpg"
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            
            # Save image
            pil_image = Image.open(io.BytesIO(image_data))
            pil_image.save(filepath, 'JPEG')
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving face image: {str(e)}")
            return None
    
    @staticmethod
    def detect_faces_in_frame(image_data):
        """
        Detect number of faces in an image frame
        
        Args:
            image_data: Binary image data
            
        Returns:
            int: Number of faces detected
        """
        try:
            pil_image = Image.open(io.BytesIO(image_data))
            image = np.array(pil_image)
            
            face_locations = face_recognition.face_locations(
                image,
                model=Config.FACE_RECOGNITION_MODEL
            )
            
            return len(face_locations)
            
        except Exception as e:
            logger.error(f"Error detecting faces: {str(e)}")
            return 0


from datetime import datetime
