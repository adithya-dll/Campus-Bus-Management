import math
from datetime import datetime, timedelta

class LocationService:
    """Service for location-based operations"""
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        Calculate distance between two GPS coordinates using Haversine formula
        
        Args:
            lat1, lon1: First coordinate
            lat2, lon2: Second coordinate
            
        Returns:
            float: Distance in kilometers
        """
        # Radius of Earth in kilometers
        R = 6371.0
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Differences
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Haversine formula
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    @staticmethod
    def calculate_eta(distance_km, average_speed_kmh=30):
        """
        Calculate estimated time of arrival
        
        Args:
            distance_km: Distance in kilometers
            average_speed_kmh: Average speed in km/h (default 30 km/h for city traffic)
            
        Returns:
            dict: {
                'eta_minutes': int,
                'eta_formatted': str,
                'distance_km': float
            }
        """
        if distance_km <= 0:
            return {
                'eta_minutes': 0,
                'eta_formatted': 'Arrived',
                'distance_km': 0
            }
        
        eta_hours = distance_km / average_speed_kmh
        eta_minutes = int(eta_hours * 60)
        
        if eta_minutes < 1:
            eta_formatted = 'Less than 1 minute'
        elif eta_minutes == 1:
            eta_formatted = '1 minute'
        elif eta_minutes < 60:
            eta_formatted = f'{eta_minutes} minutes'
        else:
            hours = eta_minutes // 60
            minutes = eta_minutes % 60
            eta_formatted = f'{hours}h {minutes}m' if minutes else f'{hours}h'
        
        return {
            'eta_minutes': eta_minutes,
            'eta_formatted': eta_formatted,
            'distance_km': round(distance_km, 2)
        }
    
    @staticmethod
    def is_near_stop(bus_lat, bus_lng, stop_lat, stop_lng, threshold_km=0.2):
        """
        Check if bus is near a stop
        
        Args:
            bus_lat, bus_lng: Bus coordinates
            stop_lat, stop_lng: Stop coordinates
            threshold_km: Distance threshold in km (default 200 meters)
            
        Returns:
            bool: True if bus is near the stop
        """
        distance = LocationService.calculate_distance(bus_lat, bus_lng, stop_lat, stop_lng)
        return distance <= threshold_km
    
    @staticmethod
    def get_next_stop(bus_location, route_stops, current_stop_index=0):
        """
        Determine the next stop based on bus location and route
        
        Args:
            bus_location: {lat, lng}
            route_stops: List of stops with {name, lat, lng, order}
            current_stop_index: Current stop index in route
            
        Returns:
            dict: {
                'next_stop': dict or None,
                'distance_km': float,
                'eta': dict
            }
        """
        if not route_stops or current_stop_index >= len(route_stops):
            return {
                'next_stop': None,
                'distance_km': 0,
                'eta': None
            }
        
        # Sort stops by order
        sorted_stops = sorted(route_stops, key=lambda x: x.get('order', 0))
        
        # Get next stop
        next_stop = sorted_stops[current_stop_index] if current_stop_index < len(sorted_stops) else None
        
        if next_stop:
            distance = LocationService.calculate_distance(
                bus_location['lat'],
                bus_location['lng'],
                next_stop['lat'],
                next_stop['lng']
            )
            
            eta = LocationService.calculate_eta(distance)
            
            return {
                'next_stop': next_stop,
                'distance_km': distance,
                'eta': eta
            }
        
        return {
            'next_stop': None,
            'distance_km': 0,
            'eta': None
        }
    
    @staticmethod
    def validate_location_update(last_location, new_location, max_speed_kmh=100, time_threshold_seconds=5):
        """
        Validate if a location update is reasonable (anti-spoofing)
        
        Args:
            last_location: {lat, lng, timestamp}
            new_location: {lat, lng, timestamp}
            max_speed_kmh: Maximum reasonable speed
            time_threshold_seconds: Minimum time between updates
            
        Returns:
            dict: {
                'valid': bool,
                'reason': str,
                'calculated_speed_kmh': float
            }
        """
        if not last_location:
            return {'valid': True, 'reason': 'First location update', 'calculated_speed_kmh': 0}
        
        try:
            # Calculate time difference
            time_diff = (new_location['timestamp'] - last_location['timestamp']).total_seconds()
            
            if time_diff < time_threshold_seconds:
                return {
                    'valid': False,
                    'reason': f'Updates too frequent (minimum {time_threshold_seconds}s)',
                    'calculated_speed_kmh': 0
                }
            
            # Calculate distance
            distance_km = LocationService.calculate_distance(
                last_location['lat'],
                last_location['lng'],
                new_location['lat'],
                new_location['lng']
            )
            
            # Calculate speed
            time_hours = time_diff / 3600
            speed_kmh = distance_km / time_hours if time_hours > 0 else 0
            
            if speed_kmh > max_speed_kmh:
                return {
                    'valid': False,
                    'reason': f'Speed too high: {speed_kmh:.1f} km/h (max: {max_speed_kmh})',
                    'calculated_speed_kmh': round(speed_kmh, 2)
                }
            
            return {
                'valid': True,
                'reason': 'Valid location update',
                'calculated_speed_kmh': round(speed_kmh, 2)
            }
            
        except Exception as e:
            return {
                'valid': False,
                'reason': f'Error validating location: {str(e)}',
                'calculated_speed_kmh': 0
            }
