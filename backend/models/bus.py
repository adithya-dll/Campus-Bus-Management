from datetime import datetime
from bson import ObjectId
from utils.database import Database

class Bus:
    """Bus model for database operations"""
    
    collection_name = 'buses'
    
    @staticmethod
    def create(bus_data):
        """Create a new bus"""
        db = Database.get_db()
        
        bus = {
            'bus_number': bus_data['bus_number'],
            'capacity': bus_data.get('capacity', 50),
            'driver_id': bus_data.get('driver_id'),
            'route_id': bus_data.get('route_id'),
            'is_active': bus_data.get('is_active', True),
            'trip_active': False,
            'current_location': bus_data.get('current_location'),
            'trip_start_time': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = db[Bus.collection_name].insert_one(bus)
        bus['_id'] = str(result.inserted_id)
        return bus
    
    @staticmethod
    def find_by_number(bus_number):
        """Find bus by bus number"""
        db = Database.get_db()
        bus = db[Bus.collection_name].find_one({'bus_number': bus_number})
        if bus:
            bus['_id'] = str(bus['_id'])
        return bus
    
    @staticmethod
    def find_all(filters=None, skip=0, limit=100):
        """Find all buses with optional filters"""
        db = Database.get_db()
        query = filters or {}
        
        cursor = db[Bus.collection_name].find(query).skip(skip).limit(limit)
        buses = []
        for bus in cursor:
            bus['_id'] = str(bus['_id'])
            buses.append(bus)
        
        return buses
    
    @staticmethod
    def update(bus_number, update_data):
        """Update bus information"""
        db = Database.get_db()
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = db[Bus.collection_name].update_one(
            {'bus_number': bus_number},
            {'$set': update_data}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def delete(bus_number):
        """Delete a bus"""
        db = Database.get_db()
        result = db[Bus.collection_name].delete_one({'bus_number': bus_number})
        return result.deleted_count > 0
    
    @staticmethod
    def update_location(bus_number, location):
        """Update bus GPS location"""
        db = Database.get_db()
        
        result = db[Bus.collection_name].update_one(
            {'bus_number': bus_number},
            {
                '$set': {
                    'current_location': location,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def start_trip(bus_number):
        """Mark bus as on trip"""
        db = Database.get_db()
        
        result = db[Bus.collection_name].update_one(
            {'bus_number': bus_number},
            {
                '$set': {
                    'trip_active': True,
                    'trip_start_time': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def end_trip(bus_number):
        """Mark bus trip as ended"""
        db = Database.get_db()
        
        result = db[Bus.collection_name].update_one(
            {'bus_number': bus_number},
            {
                '$set': {
                    'trip_active': False,
                    'trip_start_time': None,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def count(filters=None):
        """Count buses with optional filters"""
        db = Database.get_db()
        query = filters or {}
        return db[Bus.collection_name].count_documents(query)
