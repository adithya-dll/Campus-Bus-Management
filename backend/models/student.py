from datetime import datetime
from bson import ObjectId
from utils.database import Database

class Student:
    """Student model for database operations"""
    
    collection_name = 'students'
    
    @staticmethod
    def create(student_data):
        """Create a new student"""
        db = Database.get_db()
        
        student = {
            'roll_number': student_data['roll_number'],
            'name': student_data['name'],
            'email': student_data.get('email'),
            'phone': student_data.get('phone'),
            'assigned_bus': student_data.get('assigned_bus'),
            'boarding_point': student_data.get('boarding_point'),
            'face_encoding': student_data.get('face_encoding', []),
            'face_image_path': student_data.get('face_image_path'),
            'bus_pass_valid': student_data.get('bus_pass_valid', False),
            'pass_expiry': student_data.get('pass_expiry'),
            'assigned_route': student_data.get('assigned_route'),
            'is_faculty': student_data.get('is_faculty', False),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = db[Student.collection_name].insert_one(student)
        student['_id'] = str(result.inserted_id)
        return student
    
    @staticmethod
    def find_by_roll_number(roll_number):
        """Find student by roll number"""
        db = Database.get_db()
        student = db[Student.collection_name].find_one({'roll_number': roll_number})
        if student:
            student['_id'] = str(student['_id'])
        return student
    
    @staticmethod
    def find_all(filters=None, skip=0, limit=100):
        """Find all students with optional filters"""
        db = Database.get_db()
        query = filters or {}
        
        cursor = db[Student.collection_name].find(query).skip(skip).limit(limit)
        students = []
        for student in cursor:
            student['_id'] = str(student['_id'])
            students.append(student)
        
        return students
    
    @staticmethod
    def update(roll_number, update_data):
        """Update student information"""
        db = Database.get_db()
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = db[Student.collection_name].update_one(
            {'roll_number': roll_number},
            {'$set': update_data}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def delete(roll_number):
        """Delete a student"""
        db = Database.get_db()
        result = db[Student.collection_name].delete_one({'roll_number': roll_number})
        return result.deleted_count > 0
    
    @staticmethod
    def update_face_encoding(roll_number, face_encoding, image_path):
        """Update face encoding for a student"""
        db = Database.get_db()
        
        result = db[Student.collection_name].update_one(
            {'roll_number': roll_number},
            {
                '$set': {
                    'face_encoding': face_encoding,
                    'face_image_path': image_path,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def get_all_encodings():
        """Get all students with face encodings"""
        db = Database.get_db()
        students = db[Student.collection_name].find(
            {'face_encoding': {'$exists': True, '$ne': []}}
        )
        
        result = []
        for student in students:
            result.append({
                'roll_number': student['roll_number'],
                'name': student['name'],
                'face_encoding': student['face_encoding'],
                'bus_pass_valid': student.get('bus_pass_valid', False)
            })
        
        return result
    
    @staticmethod
    def count(filters=None):
        """Count students with optional filters"""
        db = Database.get_db()
        query = filters or {}
        return db[Student.collection_name].count_documents(query)
