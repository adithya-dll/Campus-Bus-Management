from flask import Blueprint, request, jsonify
from models.bus import Bus
from routes.auth import require_auth
from services.location_service import LocationService
import logging

logger = logging.getLogger(__name__)

tracking_bp = Blueprint('tracking', __name__, url_prefix='/api/tracking')

@tracking_bp.route('/update-location/<bus_number>', methods=['POST'])
@require_auth(['driver', 'admin'])
def update_location(bus_number):
    """Update bus GPS location"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'lat' not in data or 'lng' not in data:
            return jsonify({'error': 'Latitude and longitude are required'}), 400
        
        # Validate coordinates
        if not LocationService.validate_coordinates(data['lat'], data['lng']):
            return jsonify({'error': 'Invalid coordinates'}), 400
        
        # Check if bus exists
        bus = Bus.find_by_number(bus_number)
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404
        
        # Update location
        location = {
            'lat': float(data['lat']),
            'lng': float(data['lng']),
            'timestamp': data.get('timestamp')
        }
        
        success = Bus.update_location(bus_number, location)
        
        if success:
            return jsonify({'message': 'Location updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update location'}), 500
            
    except Exception as e:
        logger.error(f"Error updating location: {str(e)}")
        return jsonify({'error': 'Failed to update location'}), 500


@tracking_bp.route('/get-location/<bus_number>', methods=['GET'])
@require_auth()
def get_location(bus_number):
    """Get current bus location"""
    try:
        bus = Bus.find_by_number(bus_number)
        
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404
        
        if 'current_location' not in bus:
            return jsonify({'error': 'Location not available'}), 404
        
        return jsonify({
            'bus_number': bus_number,
            'location': bus['current_location'],
            'trip_active': bus.get('trip_active', False)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting location: {str(e)}")
        return jsonify({'error': 'Failed to get location'}), 500


@tracking_bp.route('/get-all-locations', methods=['GET'])
@require_auth()
def get_all_locations():
    """Get locations of all active buses"""
    try:
        # Get all buses
        buses = Bus.find_all({'is_active': True})
        
        # Filter to only include buses with location data
        bus_locations = []
        for bus in buses:
            if 'current_location' in bus and bus['current_location']:
                bus_locations.append({
                    'bus_number': bus['bus_number'],
                    'location': bus['current_location'],
                    'trip_active': bus.get('trip_active', False),
                    'driver_id': bus.get('driver_id'),
                    'route_id': bus.get('route_id')
                })
        
        return jsonify({'buses': bus_locations}), 200
        
    except Exception as e:
        logger.error(f"Error getting all locations: {str(e)}")
        return jsonify({'error': 'Failed to get locations'}), 500


@tracking_bp.route('/start-trip/<bus_number>', methods=['POST'])
@require_auth(['driver', 'admin'])
def start_trip(bus_number):
    """Mark bus trip as started"""
    try:
        # Check if bus exists
        bus = Bus.find_by_number(bus_number)
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404
        
        # Start trip
        success = Bus.start_trip(bus_number)
        
        if success:
            logger.info(f"Trip started for bus: {bus_number}")
            return jsonify({'message': 'Trip started successfully'}), 200
        else:
            return jsonify({'error': 'Failed to start trip'}), 500
            
    except Exception as e:
        logger.error(f"Error starting trip: {str(e)}")
        return jsonify({'error': 'Failed to start trip'}), 500


@tracking_bp.route('/end-trip/<bus_number>', methods=['POST'])
@require_auth(['driver', 'admin'])
def end_trip(bus_number):
    """Mark bus trip as ended"""
    try:
        # Check if bus exists
        bus = Bus.find_by_number(bus_number)
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404
        
        # End trip
        success = Bus.end_trip(bus_number)
        
        if success:
            logger.info(f"Trip ended for bus: {bus_number}")
            return jsonify({'message': 'Trip ended successfully'}), 200
        else:
            return jsonify({'error': 'Failed to end trip'}), 500
            
    except Exception as e:
        logger.error(f"Error ending trip: {str(e)}")
        return jsonify({'error': 'Failed to end trip'}), 500
