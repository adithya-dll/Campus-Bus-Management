from flask import Blueprint, request, jsonify
from models.route import Route
from routes.auth import require_auth
import logging

logger = logging.getLogger(__name__)

routes_bp = Blueprint('routes', __name__, url_prefix='/api/routes')

@routes_bp.route('/create', methods=['POST'])
@require_auth(['admin'])
def create_route():
    """Create a new route"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('route_id') or not data.get('route_name'):
            return jsonify({'error': 'Route ID and route name are required'}), 400
        
        # Check if route already exists
        existing = Route.find_by_id(data['route_id'])
        if existing:
            return jsonify({'error': 'Route ID already exists'}), 400
        
        # Create route
        route = Route.create(data)
        
        logger.info(f"Route created: {route['route_id']}")
        
        return jsonify({
            'message': 'Route created successfully',
            'route': route
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating route: {str(e)}")
        return jsonify({'error': 'Failed to create route'}), 500


@routes_bp.route('/update/<route_id>', methods=['PUT'])
@require_auth(['admin'])
def update_route(route_id):
    """Update route information"""
    try:
        data = request.get_json()
        
        # Check if route exists
        route = Route.find_by_id(route_id)
        if not route:
            return jsonify({'error': 'Route not found'}), 404
        
        # Update route
        success = Route.update(route_id, data)
        
        if success:
            updated_route = Route.find_by_id(route_id)
            logger.info(f"Route updated: {route_id}")
            return jsonify({
                'message': 'Route updated successfully',
                'route': updated_route
            }), 200
        else:
            return jsonify({'error': 'No changes made'}), 400
            
    except Exception as e:
        logger.error(f"Error updating route: {str(e)}")
        return jsonify({'error': 'Failed to update route'}), 500


@routes_bp.route('/get/<route_id>', methods=['GET'])
@require_auth()
def get_route(route_id):
    """Get route by ID"""
    try:
        route = Route.find_by_id(route_id)
        
        if not route:
            return jsonify({'error': 'Route not found'}), 404
        
        return jsonify({'route': route}), 200
        
    except Exception as e:
        logger.error(f"Error getting route: {str(e)}")
        return jsonify({'error': 'Failed to get route'}), 500


@routes_bp.route('/list', methods=['GET'])
@require_auth()
def list_routes():
    """List all routes with pagination"""
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 100))
        
        # Optional filters
        filters = {}
        if request.args.get('is_active') is not None:
            filters['is_active'] = request.args.get('is_active').lower() == 'true'
        
        routes = Route.find_all(filters, skip, limit)
        total = Route.count(filters)
        
        return jsonify({
            'routes': routes,
            'total': total,
            'skip': skip,
            'limit': limit
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing routes: {str(e)}")
        return jsonify({'error': 'Failed to list routes'}), 500


@routes_bp.route('/delete/<route_id>', methods=['DELETE'])
@require_auth(['admin'])
def delete_route(route_id):
    """Delete a route"""
    try:
        success = Route.delete(route_id)
        
        if success:
            logger.info(f"Route deleted: {route_id}")
            return jsonify({'message': 'Route deleted successfully'}), 200
        else:
            return jsonify({'error': 'Route not found'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting route: {str(e)}")
        return jsonify({'error': 'Failed to delete route'}), 500
