class Bus {
  final String busNumber;
  final int capacity;
  final String? routeId;
  final bool tripActive;

  Bus({
    required this.busNumber,
    required this.capacity,
    this.routeId,
    required this.tripActive,
  });

  factory Bus.fromJson(Map<String, dynamic> json) {
    return Bus(
      busNumber: json['bus_number'] ?? '',
      capacity: json['capacity'] ?? 50,
      routeId: json['route_id'],
      tripActive: json['trip_active'] ?? false,
    );
  }
}
