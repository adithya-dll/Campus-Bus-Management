from flask import Blueprint, request, jsonify
from models.driver import Driver
from routes.auth import require_auth
from utils.validators import validate_required_fields, validate_email, sanitize_string
import logging

logger = logging.getLogger(__name__)

drivers_bp = Blueprint('drivers', __name__, url_prefix='/api/drivers')

@drivers_bp.route('/register', methods=['POST'])
@require_auth(['admin'])
@validate_required_fields(['driver_id', 'name', 'phone', 'password'])
def register_driver():
    """Register a new driver"""
    try:
        data = request.get_json()
        
        # Check if driver already exists
        existing = Driver.find_by_id(data['driver_id'])
        if existing:
            return jsonify({'error': 'Driver ID already exists'}), 400
        
        # Validate email if provided
        if data.get('email') and not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Sanitize inputs
        data['name'] = sanitize_string(data['name'])
        
        # TODO: Hash password before storing (use bcrypt or similar)
        # For now, storing plain text for simplicity
        
        # Create driver
        driver = Driver.create(data)
        
        # Remove password from response
        driver.pop('password', None)
        
        logger.info(f"Driver registered: {driver['driver_id']}")
        
        return jsonify({
            'message': 'Driver registered successfully',
            'driver': driver
        }), 201
        
    except Exception as e:
        logger.error(f"Error registering driver: {str(e)}")
        return jsonify({'error': 'Failed to register driver'}), 500


@drivers_bp.route('/update/<driver_id>', methods=['PUT'])
@require_auth(['admin'])
def update_driver(driver_id):
    """Update driver information"""
    try:
        data = request.get_json()
        
        # Check if driver exists
        driver = Driver.find_by_id(driver_id)
        if not driver:
            return jsonify({'error': 'Driver not found'}), 404
        
        # Validate email if provided
        if data.get('email') and not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Sanitize inputs
        if 'name' in data:
            data['name'] = sanitize_string(data['name'])
        
        # Update driver
        success = Driver.update(driver_id, data)
        
        if success:
            updated_driver = Driver.find_by_id(driver_id)
            updated_driver.pop('password', None)
            logger.info(f"Driver updated: {driver_id}")
            return jsonify({
                'message': 'Driver updated successfully',
                'driver': updated_driver
            }), 200
        else:
            return jsonify({'error': 'No changes made'}), 400
            
    except Exception as e:
        logger.error(f"Error updating driver: {str(e)}")
        return jsonify({'error': 'Failed to update driver'}), 500


@drivers_bp.route('/get/<driver_id>', methods=['GET'])
@require_auth()
def get_driver(driver_id):
    """Get driver by ID"""
    try:
        driver = Driver.find_by_id(driver_id)
        
        if not driver:
            return jsonify({'error': 'Driver not found'}), 404
        
        # Remove password
        driver.pop('password', None)
        
        return jsonify({'driver': driver}), 200
        
    except Exception as e:
        logger.error(f"Error getting driver: {str(e)}")
        return jsonify({'error': 'Failed to get driver'}), 500


@drivers_bp.route('/list', methods=['GET'])
@require_auth(['admin'])
def list_drivers():
    """List all drivers"""
    try:
        filters = {}
        
        if request.args.get('is_active') is not None:
            filters['is_active'] = request.args.get('is_active').lower() == 'true'
        
        drivers = Driver.find_all(filters)
        total = Driver.count(filters)
        
        return jsonify({
            'drivers': drivers,
            'total': total
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing drivers: {str(e)}")
        return jsonify({'error': 'Failed to list drivers'}), 500


@drivers_bp.route('/delete/<driver_id>', methods=['DELETE'])
@require_auth(['admin'])
def delete_driver(driver_id):
    """Delete a driver"""
    try:
        success = Driver.delete(driver_id)
        
        if success:
            logger.info(f"Driver deleted: {driver_id}")
            return jsonify({'message': 'Driver deleted successfully'}), 200
        else:
            return jsonify({'error': 'Driver not found'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting driver: {str(e)}")
        return jsonify({'error': 'Failed to delete driver'}), 500
