class BusRoute {
  final String routeId;
  final String routeName;
  final List<String> boardingPoints;
  final double distanceKm;
  final int estimatedDurationMinutes;

  BusRoute({
    required this.routeId,
    required this.routeName,
    required this.boardingPoints,
    required this.distanceKm,
    required this.estimatedDurationMinutes,
  });

  factory BusRoute.fromJson(Map<String, dynamic> json) {
    return BusRoute(
      routeId: json['route_id'] ?? '',
      routeName: json['route_name'] ?? '',
      boardingPoints: (json['boarding_points'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      distanceKm: (json['distance_km'] ?? 0.0).toDouble(),
      estimatedDurationMinutes: json['estimated_duration_minutes'] ?? 0,
    );
  }
}
