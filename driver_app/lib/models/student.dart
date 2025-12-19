class Student {
  final String rollNumber;
  final String name;
  final String assignedBus;
  final String boardingPoint;
  final bool busPassValid;
  final bool boarded;
  final String? boardedAt;

  Student({
    required this.rollNumber,
    required this.name,
    required this.assignedBus,
    required this.boardingPoint,
    required this.busPassValid,
    this.boarded = false,
    this.boardedAt,
  });

  factory Student.fromJson(Map<String, dynamic> json) {
    return Student(
      rollNumber: json['roll_number'] ?? '',
      name: json['name'] ?? '',
      assignedBus: json['assigned_bus'] ?? '',
      boardingPoint: json['boarding_point'] ?? '',
      busPassValid: json['bus_pass_valid'] ?? false,
      boarded: json['boarded'] ?? false,
      boardedAt: json['boarded_at'],
    );
  }
}
