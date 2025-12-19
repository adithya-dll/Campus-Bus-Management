class Student {
  final String rollNumber;
  final String name;
  final String email;
  final String phone;
  final String assignedBus;
  final String boardingPoint;
  final bool busPassValid;
  final String? passExpiry;

  Student({
    required this.rollNumber,
    required this.name,
    required this.email,
    required this.phone,
    required this.assignedBus,
    required this.boardingPoint,
    required this.busPassValid,
    this.passExpiry,
  });

  factory Student.fromJson(Map<String, dynamic> json) {
    return Student(
      rollNumber: json['roll_number'] ?? '',
      name: json['name'] ?? '',
      email: json['email'] ?? '',
      phone: json['phone'] ?? '',
      assignedBus: json['assigned_bus'] ?? '',
      boardingPoint: json['boarding_point'] ?? '',
      busPassValid: json['bus_pass_valid'] ?? false,
      passExpiry: json['pass_expiry'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'roll_number': rollNumber,
      'name': name,
      'email': email,
      'phone': phone,
      'assigned_bus': assignedBus,
      'boarding_point': boardingPoint,
      'bus_pass_valid': busPassValid,
      'pass_expiry': passExpiry,
    };
  }
}
