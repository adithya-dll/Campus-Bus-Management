class Bus {
  final String busNumber;
  final int capacity;
  final String? driverId;
  final String? routeId;
  final bool isActive;
  final bool tripActive;
  final BusLocation? currentLocation;

  Bus({
    required this.busNumber,
    required this.capacity,
    this.driverId,
    this.routeId,
    required this.isActive,
    required this.tripActive,
    this.currentLocation,
  });

  factory Bus.fromJson(Map<String, dynamic> json) {
    return Bus(
      busNumber: json['bus_number'] ?? '',
      capacity: json['capacity'] ?? 50,
      driverId: json['driver_id'],
      routeId: json['route_id'],
      isActive: json['is_active'] ?? true,
      tripActive: json['trip_active'] ?? false,
      currentLocation: json['current_location'] != null
          ? BusLocation.fromJson(json['current_location'])
          : null,
    );
  }
}

class BusLocation {
  final double lat;
  final double lng;
  final String? timestamp;

  BusLocation({
    required this.lat,
    required this.lng,
    this.timestamp,
  });

  factory BusLocation.fromJson(Map<String, dynamic> json) {
    return BusLocation(
      lat: (json['lat'] ?? 0.0).toDouble(),
      lng: (json['lng'] ?? 0.0).toDouble(),
      timestamp: json['timestamp'],
    );
  }
}
