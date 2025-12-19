from flask import Blueprint, request, jsonify
from models.log import Log
from routes.auth import require_auth
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

logs_bp = Blueprint('logs', __name__, url_prefix='/api/logs')

@logs_bp.route('/entry', methods=['GET'])
@require_auth()
def get_entry_logs():
    """Get entry verification logs with optional filters"""
    try:
        # Parse query parameters
        bus_id = request.args.get('bus_id')
        student_id = request.args.get('student_id')
        
        # Date filters
        start_date = None
        end_date = None
        
        if request.args.get('start_date'):
            try:
                start_date = datetime.fromisoformat(request.args.get('start_date'))
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use ISO format'}), 400
        
        if request.args.get('end_date'):
            try:
                end_date = datetime.fromisoformat(request.args.get('end_date'))
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use ISO format'}), 400
        
        # Get logs
        logs = Log.get_entry_logs(bus_id, student_id, start_date, end_date)
        
        return jsonify({
            'logs': logs,
            'total': len(logs)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting entry logs: {str(e)}")
        return jsonify({'error': 'Failed to get entry logs'}), 500


@logs_bp.route('/alerts', methods=['GET'])
@require_auth()
def get_alerts():
    """Get security alerts with optional resolved filter"""
    try:
        resolved = None
        if request.args.get('resolved') is not None:
            resolved = request.args.get('resolved').lower() == 'true'
        
        alerts = Log.get_alerts(resolved)
        
        return jsonify({
            'alerts': alerts,
            'total': len(alerts)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting alerts: {str(e)}")
        return jsonify({'error': 'Failed to get alerts'}), 500


@logs_bp.route('/alerts/resolve/<alert_id>', methods=['PUT'])
@require_auth(['admin'])
def resolve_alert(alert_id):
    """Mark an alert as resolved"""
    try:
        success = Log.resolve_alert(alert_id)
        
        if success:
            logger.info(f"Alert resolved: {alert_id}")
            return jsonify({'message': 'Alert resolved successfully'}), 200
        else:
            return jsonify({'error': 'Alert not found'}), 404
            
    except Exception as e:
        logger.error(f"Error resolving alert: {str(e)}")
        return jsonify({'error': 'Failed to resolve alert'}), 500


@logs_bp.route('/statistics', methods=['GET'])
@require_auth(['admin'])
def get_statistics():
    """Get verification statistics"""
    try:
        # Date range (default: last 7 days)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        if request.args.get('start_date'):
            try:
                start_date = datetime.fromisoformat(request.args.get('start_date'))
            except ValueError:
                pass
        
        if request.args.get('end_date'):
            try:
                end_date = datetime.fromisoformat(request.args.get('end_date'))
            except ValueError:
                pass
        
        # Get statistics
        stats = Log.get_statistics(start_date, end_date)
        
        # Get counts for different log types
        from models.student import Student
        from models.bus import Bus
        from models.driver import Driver
        
        total_students = Student.count()
        total_buses = Bus.count()
        total_drivers = Driver.count()
        active_buses = Bus.count({'is_active': True})
        buses_on_trip = Bus.count({'trip_active': True})
        
        return jsonify({
            'verification_stats': stats,
            'system_stats': {
                'total_students': total_students,
                'total_buses': total_buses,
                'total_drivers': total_drivers,
                'active_buses': active_buses,
                'buses_on_trip': buses_on_trip
            },
            'date_range': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return jsonify({'error': 'Failed to get statistics'}), 500


@logs_bp.route('/create-alert', methods=['POST'])
@require_auth(['driver', 'admin'])
def create_alert():
    """Manually create an alert (e.g., emergency button)"""
    try:
        from flask import session
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        alert_data = {
            'alert_type': data.get('alert_type', 'emergency'),
            'severity': data.get('severity', 'high'),
            'bus_id': data.get('bus_id'),
            'driver_id': session.get('user_id'),
            'student_id': data.get('student_id'),
            'message': data['message'],
            'location': data.get('location', {})
        }
        
        alert = Log.create_alert(alert_data)
        
        logger.warning(f"Alert created: {alert['alert_type']} - {alert['message']}")
        
        # TODO: Send emergency notifications to admins
        # from services.notification_service import NotificationService
        # NotificationService.notify_emergency(admin_ids, alert_data['bus_id'], alert_data['driver_id'], alert_data['message'])
        
        return jsonify({
            'message': 'Alert created successfully',
            'alert': alert
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating alert: {str(e)}")
        return jsonify({'error': 'Failed to create alert'}), 500
