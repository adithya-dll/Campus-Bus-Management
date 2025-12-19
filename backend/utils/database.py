from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database handler"""
    
    _client = None
    _db = None
    
    @classmethod
    def initialize(cls):
        """Initialize MongoDB connection"""
        try:
            cls._client = MongoClient(Config.MONGODB_URI)
            # Test connection
            cls._client.admin.command('ping')
            cls._db = cls._client[Config.DATABASE_NAME]
            logger.info(f"Connected to MongoDB: {Config.DATABASE_NAME}")
            
            # Create indexes
            cls._create_indexes()
            
            return True
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
    
    @classmethod
    def _create_indexes(cls):
        """Create database indexes for better performance"""
        try:
            # Students collection indexes
            cls._db.students.create_index("student_id", unique=True)
            cls._db.students.create_index("email", unique=True, sparse=True)
            
            # Buses collection indexes
            cls._db.buses.create_index("bus_id", unique=True)
            cls._db.buses.create_index("driver_id")
            
            # Routes collection indexes
            cls._db.routes.create_index("route_id", unique=True)
            
            # Drivers collection indexes
            cls._db.drivers.create_index("driver_id", unique=True)
            cls._db.drivers.create_index("email", unique=True, sparse=True)
            
            # Logs collection indexes
            cls._db.logs.create_index("timestamp")
            cls._db.logs.create_index("student_id")
            cls._db.logs.create_index("bus_id")
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.warning(f"Error creating indexes: {e}")
    
    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls._db is None:
            cls.initialize()
        return cls._db
    
    @classmethod
    def close(cls):
        """Close database connection"""
        if cls._client:
            cls._client.close()
            logger.info("MongoDB connection closed")
