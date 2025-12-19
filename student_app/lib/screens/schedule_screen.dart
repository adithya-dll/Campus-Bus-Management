import 'package:flutter/material.dart';
import '../models/student.dart';
import '../models/route.dart';

class ScheduleScreen extends StatelessWidget {
  final BusRoute route;
  final Student student;

  const ScheduleScreen({
    super.key,
    required this.route,
    required this.student,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Route Schedule'),
        backgroundColor: Colors.orange.shade700,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Route Info Card
            Card(
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.route, color: Colors.orange.shade700, size: 28),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            route.routeName,
                            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                                  fontWeight: FontWeight.bold,
                                ),
                          ),
                        ),
                      ],
                    ),
                    if (route.description.isNotEmpty) ...[
                      const SizedBox(height: 8),
                      Text(
                        route.description,
                        style: TextStyle(color: Colors.grey.shade600),
                      ),
                    ],
                    const Divider(height: 32),
                    Row(
                      children: [
                        Expanded(
                          child: _buildInfoItem(
                            icon: Icons.straighten,
                            label: 'Distance',
                            value: '${route.distanceKm} km',
                          ),
                        ),
                        Expanded(
                          child: _buildInfoItem(
                            icon: Icons.access_time,
                            label: 'Duration',
                            value: '${route.estimatedDurationMinutes} min',
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Boarding Points Section
            Text(
              'Boarding Points',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 12),

            // Boarding Points List
            Card(
              elevation: 2,
              child: ListView.separated(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: route.boardingPoints.length,
                separatorBuilder: (context, index) => const Divider(height: 1),
                itemBuilder: (context, index) {
                  final point = route.boardingPoints[index];
                  final isStudentPoint = point == student.boardingPoint;
                  final stopNumber = index + 1;

                  return Container(
                    color: isStudentPoint
                        ? Colors.orange.shade50
                        : Colors.transparent,
                    child: ListTile(
                      leading: Container(
                        width: 40,
                        height: 40,
                        decoration: BoxDecoration(
                          color: isStudentPoint
                              ? Colors.orange.shade700
                              : Colors.grey.shade300,
                          shape: BoxShape.circle,
                        ),
                        child: Center(
                          child: Text(
                            '$stopNumber',
                            style: TextStyle(
                              color: isStudentPoint
                                  ? Colors.white
                                  : Colors.black87,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                      title: Text(
                        point,
                        style: TextStyle(
                          fontWeight: isStudentPoint
                              ? FontWeight.bold
                              : FontWeight.normal,
                        ),
                      ),
                      trailing: isStudentPoint
                          ? Chip(
                              label: const Text(
                                'Your Stop',
                                style: TextStyle(color: Colors.white),
                              ),
                              backgroundColor: Colors.orange.shade700,
                            )
                          : null,
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 24),

            // Additional Info
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.info_outline, color: Colors.blue.shade700),
                        const SizedBox(width: 8),
                        Text(
                          'Travel Tips',
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.bold,
                              ),
                        ),
                      ],
                    ),
                    const Divider(height: 24),
                    _buildTipRow('Be at your boarding point 5 minutes early'),
                    const SizedBox(height: 8),
                    _buildTipRow('Have your bus pass QR code ready'),
                    const SizedBox(height: 8),
                    _buildTipRow('Track your bus in real-time from the home screen'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoItem({
    required IconData icon,
    required String label,
    required String value,
  }) {
    return Column(
      children: [
        Icon(icon, color: Colors.orange.shade700),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: Colors.grey.shade600,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          value,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  Widget _buildTipRow(String text) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Icon(Icons.check_circle, color: Colors.green, size: 20),
        const SizedBox(width: 8),
        Expanded(child: Text(text)),
      ],
    );
  }
}
