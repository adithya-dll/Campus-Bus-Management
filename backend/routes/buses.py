from flask import Blueprint, request, jsonify
from models.bus import Bus
from routes.auth import require_auth
import logging

logger = logging.getLogger(__name__)

buses_bp = Blueprint('buses', __name__, url_prefix='/api/buses')

@buses_bp.route('/create', methods=['POST'])
@require_auth(['admin'])
def create_bus():
    """Create a new bus"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('bus_number'):
            return jsonify({'error': 'Bus number is required'}), 400
        
        # Check if bus already exists
        existing = Bus.find_by_number(data['bus_number'])
        if existing:
            return jsonify({'error': 'Bus number already exists'}), 400
        
        # Create bus
        bus = Bus.create(data)
        
        logger.info(f"Bus created: {bus['bus_number']}")
        
        return jsonify({
            'message': 'Bus created successfully',
            'bus': bus
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating bus: {str(e)}")
        return jsonify({'error': 'Failed to create bus'}), 500


@buses_bp.route('/update/<bus_number>', methods=['PUT'])
@require_auth(['admin'])
def update_bus(bus_number):
    """Update bus information"""
    try:
        data = request.get_json()
        
        # Check if bus exists
        bus = Bus.find_by_number(bus_number)
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404
        
        # Handle driver assignment/un-assignment
        if 'driver_id' in data:
            from models.driver import Driver
            
            # If old driver exists, clear their assignment
            if bus.get('driver_id'):
                old_driver = Driver.find_by_id(bus['driver_id'])
                if old_driver:
                    Driver.update(bus['driver_id'], {'assigned_bus': ''})
            
            # If new driver exists, set their assignment
            if data['driver_id']:
                new_driver = Driver.find_by_id(data['driver_id'])
                if new_driver:
                    Driver.update(data['driver_id'], {'assigned_bus': bus_number})
        
        # Handle route assignment/un-assignment
        if 'route_id' in data:
            from models.route import Route
            
            # If old route exists, clear its assignment
            if bus.get('route_id'):
                old_route = Route.find_by_id(bus['route_id'])
                if old_route:
                    Route.update(bus['route_id'], {'assigned_bus': ''})
            
            # If new route exists, set its assignment
            if data['route_id']:
                new_route = Route.find_by_id(data['route_id'])
                if new_route:
                    Route.update(data['route_id'], {'assigned_bus': bus_number})
        
        # Update bus
        success = Bus.update(bus_number, data)
        
        if success:
            updated_bus = Bus.find_by_number(bus_number)
            logger.info(f"Bus updated: {bus_number}")
            return jsonify({
                'message': 'Bus updated successfully',
                'bus': updated_bus
            }), 200
        else:
            return jsonify({'error': 'No changes made'}), 400
            
    except Exception as e:
        logger.error(f"Error updating bus: {str(e)}")
        return jsonify({'error': 'Failed to update bus'}), 500


@buses_bp.route('/get/<bus_number>', methods=['GET'])
@require_auth()
def get_bus(bus_number):
    """Get bus by number"""
    try:
        bus = Bus.find_by_number(bus_number)
        
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404
        
        return jsonify({'bus': bus}), 200
        
    except Exception as e:
        logger.error(f"Error getting bus: {str(e)}")
        return jsonify({'error': 'Failed to get bus'}), 500


@buses_bp.route('/list', methods=['GET'])
@require_auth()
def list_buses():
    """List all buses with pagination"""
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 100))
        
        # Optional filters
        filters = {}
        if request.args.get('route_id'):
            filters['route_id'] = request.args.get('route_id')
        if request.args.get('is_active') is not None:
            filters['is_active'] = request.args.get('is_active').lower() == 'true'
        if request.args.get('trip_active') is not None:
            filters['trip_active'] = request.args.get('trip_active').lower() == 'true'
        
        buses = Bus.find_all(filters, skip, limit)
        total = Bus.count(filters)
        
        return jsonify({
            'buses': buses,
            'total': total,
            'skip': skip,
            'limit': limit
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing buses: {str(e)}")
        return jsonify({'error': 'Failed to list buses'}), 500


@buses_bp.route('/delete/<bus_number>', methods=['DELETE'])
@require_auth(['admin'])
def delete_bus(bus_number):
    """Delete a bus"""
    try:
        success = Bus.delete(bus_number)
        
        if success:
            logger.info(f"Bus deleted: {bus_number}")
            return jsonify({'message': 'Bus deleted successfully'}), 200
        else:
            return jsonify({'error': 'Bus not found'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting bus: {str(e)}")
        return jsonify({'error': 'Failed to delete bus'}), 500


@buses_bp.route('/assign-driver/<bus_number>', methods=['PUT'])
@require_auth(['admin'])
def assign_driver(bus_number):
    """Assign driver to bus"""
    try:
        data = request.get_json()
        driver_id = data.get('driver_id')
        
        if not driver_id:
            return jsonify({'error': 'Driver ID is required'}), 400
        
        # Check if bus exists
        bus = Bus.find_by_number(bus_number)
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404
        
        # Check if driver exists
        from models.driver import Driver
        driver = Driver.find_by_id(driver_id)
        if not driver:
            return jsonify({'error': 'Driver not found'}), 404
        
        # Update bus with driver assignment
        bus_success = Bus.update(bus_number, {'driver_id': driver_id})
        
        # Update driver with bus assignment
        driver_success = Driver.update(driver_id, {'assigned_bus': bus_number})
        
        if bus_success and driver_success:
            logger.info(f"Driver {driver_id} assigned to bus {bus_number}")
            return jsonify({'message': 'Driver assigned successfully'}), 200
        else:
            return jsonify({'error': 'Failed to assign driver'}), 500
            
    except Exception as e:
        logger.error(f"Error assigning driver: {str(e)}")
        return jsonify({'error': 'Failed to assign driver'}), 500


@buses_bp.route('/assign-route/<bus_number>', methods=['PUT'])
@require_auth(['admin'])
def assign_route(bus_number):
    """Assign route to bus"""
    try:
        data = request.get_json()
        route_id = data.get('route_id')
        
        if not route_id:
            return jsonify({'error': 'Route ID is required'}), 400
        
        # Check if bus exists
        bus = Bus.find_by_number(bus_number)
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404
        
        # Update route assignment
        success = Bus.update(bus_number, {'route_id': route_id})
        
        if success:
            logger.info(f"Route {route_id} assigned to bus {bus_number}")
            return jsonify({'message': 'Route assigned successfully'}), 200
        else:
            return jsonify({'error': 'Failed to assign route'}), 500
            
    except Exception as e:
        logger.error(f"Error assigning route: {str(e)}")
        return jsonify({'error': 'Failed to assign route'}), 500
