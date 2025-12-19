from datetime import datetime
from utils.database import Database

class Driver:
    """Driver model for database operations"""
    
    collection_name = 'drivers'
    
    @staticmethod
    def create(driver_data):
        """Create a new driver"""
        db = Database.get_db()
        
        driver = {
            'driver_id': driver_data['driver_id'],
            'name': driver_data['name'],
            'email': driver_data.get('email'),
            'phone': driver_data['phone'],
            'license_number': driver_data.get('license_number'),
            'password': driver_data['password'],  # Should be hashed before storing
            'assigned_bus': driver_data.get('assigned_bus'),
            'is_active': driver_data.get('is_active', True),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = db[Driver.collection_name].insert_one(driver)
        driver['_id'] = str(result.inserted_id)
        return driver
    
    @staticmethod
    def find_by_id(driver_id):
        """Find driver by driver ID"""
        db = Database.get_db()
        driver = db[Driver.collection_name].find_one({'driver_id': driver_id})
        if driver:
            driver['_id'] = str(driver['_id'])
        return driver
    
    @staticmethod
    def find_by_credentials(driver_id, password):
        """Find driver by credentials (for login)"""
        db = Database.get_db()
        driver = db[Driver.collection_name].find_one({
            'driver_id': driver_id,
            'password': password  # In production, compare hashed passwords
        })
        if driver:
            driver['_id'] = str(driver['_id'])
        return driver
    
    @staticmethod
    def find_all(filters=None):
        """Find all drivers with optional filters"""
        db = Database.get_db()
        query = filters or {}
        
        cursor = db[Driver.collection_name].find(query)
        drivers = []
        for driver in cursor:
            driver['_id'] = str(driver['_id'])
            # Remove password from response
            driver.pop('password', None)
            drivers.append(driver)
        
        return drivers
    
    @staticmethod
    def update(driver_id, update_data):
        """Update driver information"""
        db = Database.get_db()
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = db[Driver.collection_name].update_one(
            {'driver_id': driver_id},
            {'$set': update_data}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def delete(driver_id):
        """Delete a driver"""
        db = Database.get_db()
        result = db[Driver.collection_name].delete_one({'driver_id': driver_id})
        return result.deleted_count > 0
    
    @staticmethod
    def count(filters=None):
        """Count drivers with optional filters"""
        db = Database.get_db()
        query = filters or {}
        return db[Driver.collection_name].count_documents(query)
