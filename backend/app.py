from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from utils.database import Database
import logging
from datetime import timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    Config.init_app(app)
    
    # Configure session
    app.secret_key = Config.SECRET_KEY
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=Config.PERMANENT_SESSION_LIFETIME)
    
    # Enable CORS
    CORS(app, 
         origins=Config.CORS_ORIGINS,
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Initialize database
    logger.info("Initializing database connection...")
    if not Database.initialize():
        logger.error("Failed to connect to database")
        raise Exception("Database connection failed")
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.students import students_bp
    from routes.buses import buses_bp
    from routes.routes import routes_bp
    from routes.drivers import drivers_bp
    from routes.tracking import tracking_bp
    from routes.face_recognition import face_bp
    from routes.logs import logs_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(buses_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(tracking_bp)
    app.register_blueprint(face_bp)
    app.register_blueprint(logs_bp)
    
    logger.info("All blueprints registered successfully")
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Campus Bus Management System API',
            'version': '1.0.0',
            'status': 'running'
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        try:
            # Check database connection
            db = Database.get_db()
            db.command('ping')
            
            return jsonify({
                'status': 'healthy',
                'database': 'connected'
            }), 200
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            }), 500
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled exception: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    logger.info(f"Starting Campus Bus Management System API")
    logger.info(f"Host: {Config.HOST}")
    logger.info(f"Port: {Config.PORT}")
    logger.info(f"Debug: {Config.DEBUG}")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
