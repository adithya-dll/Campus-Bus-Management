from datetime import datetime
from bson import ObjectId
from utils.database import Database

class Route:
    """Route model for database operations"""
    
    collection_name = 'routes'
    
    @staticmethod
    def create(route_data):
        """Create a new route"""
        db = Database.get_db()
        
        route = {
            'route_id': route_data['route_id'],
            'route_name': route_data['route_name'],
            'description': route_data.get('description', ''),
            'assigned_bus': route_data.get('assigned_bus'),
            'boarding_points': route_data.get('boarding_points', []),
            'distance_km': route_data.get('distance_km', 0),
            'estimated_duration_minutes': route_data.get('estimated_duration_minutes', 0),
            'is_active': route_data.get('is_active', True),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = db[Route.collection_name].insert_one(route)
        route['_id'] = str(result.inserted_id)
        return route
    
    @staticmethod
    def find_by_id(route_id):
        """Find route by ID"""
        db = Database.get_db()
        route = db[Route.collection_name].find_one({'route_id': route_id})
        if route:
            route['_id'] = str(route['_id'])
        return route
    
    @staticmethod
    def find_all(filters=None, skip=0, limit=100):
        """Find all routes with optional filters"""
        db = Database.get_db()
        query = filters or {}
        
        cursor = db[Route.collection_name].find(query).skip(skip).limit(limit)
        routes = []
        for route in cursor:
            route['_id'] = str(route['_id'])
            routes.append(route)
        
        return routes
    
    @staticmethod
    def update(route_id, update_data):
        """Update route information"""
        db = Database.get_db()
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = db[Route.collection_name].update_one(
            {'route_id': route_id},
            {'$set': update_data}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def delete(route_id):
        """Delete a route"""
        db = Database.get_db()
        result = db[Route.collection_name].delete_one({'route_id': route_id})
        return result.deleted_count > 0
    
    @staticmethod
    def count(filters=None):
        """Count routes with optional filters"""
        db = Database.get_db()
        query = filters or {}
        return db[Route.collection_name].count_documents(query)
