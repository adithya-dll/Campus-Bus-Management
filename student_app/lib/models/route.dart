class BusRoute {
  final String routeId;
  final String routeName;
  final String description;
  final String? assignedBus;
  final List<String> boardingPoints;
  final double distanceKm;
  final int estimatedDurationMinutes;
  final bool isActive;

  BusRoute({
    required this.routeId,
    required this.routeName,
    required this.description,
    this.assignedBus,
    required this.boardingPoints,
    required this.distanceKm,
    required this.estimatedDurationMinutes,
    required this.isActive,
  });

  factory BusRoute.fromJson(Map<String, dynamic> json) {
    return BusRoute(
      routeId: json['route_id'] ?? '',
      routeName: json['route_name'] ?? '',
      description: json['description'] ?? '',
      assignedBus: json['assigned_bus'],
      boardingPoints: (json['boarding_points'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      distanceKm: (json['distance_km'] ?? 0.0).toDouble(),
      estimatedDurationMinutes: json['estimated_duration_minutes'] ?? 0,
      isActive: json['is_active'] ?? true,
    );
  }
}
