from datetime import datetime
from utils.database import Database

class Log:
    """Log model for entry verification and security events"""
    
    collection_name = 'logs'
    
    @staticmethod
    def create_entry_log(log_data):
        """Create entry verification log"""
        db = Database.get_db()
        
        log = {
            'type': 'entry_verification',
            'timestamp': datetime.utcnow(),
            'student_id': log_data.get('student_id'),
            'student_name': log_data.get('student_name'),
            'bus_id': log_data['bus_id'],
            'driver_id': log_data.get('driver_id'),
            'status': log_data['status'],  # 'valid', 'invalid_face', 'invalid_pass', 'not_found'
            'confidence': log_data.get('confidence'),  # Face match confidence
            'image_path': log_data.get('image_path'),
            'location': log_data.get('location', {}),
            'notes': log_data.get('notes', '')
        }
        
        result = db[Log.collection_name].insert_one(log)
        log['_id'] = str(result.inserted_id)
        return log
    
    @staticmethod
    def create_alert(alert_data):
        """Create security alert"""
        db = Database.get_db()
        
        alert = {
            'type': 'alert',
            'timestamp': datetime.utcnow(),
            'alert_type': alert_data['alert_type'],  # 'invalid_entry', 'emergency', 'system'
            'severity': alert_data.get('severity', 'medium'),  # 'low', 'medium', 'high'
            'bus_id': alert_data.get('bus_id'),
            'driver_id': alert_data.get('driver_id'),
            'student_id': alert_data.get('student_id'),
            'message': alert_data['message'],
            'location': alert_data.get('location', {}),
            'resolved': False
        }
        
        result = db[Log.collection_name].insert_one(alert)
        alert['_id'] = str(result.inserted_id)
        return alert
    
    @staticmethod
    def find_logs(filters=None, skip=0, limit=100):
        """Find logs with optional filters"""
        db = Database.get_db()
        query = filters or {}
        
        cursor = db[Log.collection_name].find(query).sort('timestamp', -1).skip(skip).limit(limit)
        logs = []
        for log in cursor:
            log['_id'] = str(log['_id'])
            logs.append(log)
        
        return logs
    
    @staticmethod
    def get_entry_logs(bus_id=None, student_id=None, start_date=None, end_date=None):
        """Get entry verification logs with filters"""
        query = {'type': 'entry_verification'}
        
        if bus_id:
            query['bus_id'] = bus_id
        if student_id:
            query['student_id'] = student_id
        if start_date or end_date:
            query['timestamp'] = {}
            if start_date:
                query['timestamp']['$gte'] = start_date
            if end_date:
                query['timestamp']['$lte'] = end_date
        
        return Log.find_logs(query)
    
    @staticmethod
    def get_alerts(resolved=None):
        """Get alerts with optional resolved filter"""
        query = {'type': 'alert'}
        
        if resolved is not None:
            query['resolved'] = resolved
        
        return Log.find_logs(query)
    
    @staticmethod
    def resolve_alert(alert_id):
        """Mark an alert as resolved"""
        db = Database.get_db()
        from bson import ObjectId
        
        result = db[Log.collection_name].update_one(
            {'_id': ObjectId(alert_id)},
            {'$set': {'resolved': True, 'resolved_at': datetime.utcnow()}}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def get_statistics(start_date=None, end_date=None):
        """Get verification statistics"""
        db = Database.get_db()
        
        match_query = {'type': 'entry_verification'}
        if start_date or end_date:
            match_query['timestamp'] = {}
            if start_date:
                match_query['timestamp']['$gte'] = start_date
            if end_date:
                match_query['timestamp']['$lte'] = end_date
        
        pipeline = [
            {'$match': match_query},
            {
                '$group': {
                    '_id': '$status',
                    'count': {'$sum': 1}
                }
            }
        ]
        
        results = db[Log.collection_name].aggregate(pipeline)
        stats = {item['_id']: item['count'] for item in results}
        
        return stats
    
    @staticmethod
    def count(filters=None):
        """Count logs with optional filters"""
        db = Database.get_db()
        query = filters or {}
        return db[Log.collection_name].count_documents(query)
