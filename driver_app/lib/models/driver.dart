class Driver {
  final String driverId;
  final String name;
  final String phone;
  final String licenseNumber;
  final String assignedBus;
  final bool isActive;

  Driver({
    required this.driverId,
    required this.name,
    required this.phone,
    required this.licenseNumber,
    required this.assignedBus,
    required this.isActive,
  });

  factory Driver.fromJson(Map<String, dynamic> json) {
    return Driver(
      driverId: json['driver_id'] ?? '',
      name: json['name'] ?? '',
      phone: json['phone'] ?? '',
      licenseNumber: json['license_number'] ?? '',
      assignedBus: json['assigned_bus'] ?? '',
      isActive: json['is_active'] ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'driver_id': driverId,
      'name': name,
      'phone': phone,
      'license_number': licenseNumber,
      'assigned_bus': assignedBus,
      'is_active': isActive,
    };
  }
}
