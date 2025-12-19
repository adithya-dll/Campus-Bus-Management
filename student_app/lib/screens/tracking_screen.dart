import 'package:flutter/material.dart';
import 'dart:async';
import '../models/bus.dart';
import '../models/student.dart';
import '../models/route.dart';
import '../services/api_service.dart';

class TrackingScreen extends StatefulWidget {
  final Bus bus;
  final Student student;
  final BusRoute? route;

  const TrackingScreen({
    super.key,
    required this.bus,
    required this.student,
    this.route,
  });

  @override
  State<TrackingScreen> createState() => _TrackingScreenState();
}

class _TrackingScreenState extends State<TrackingScreen> {
  BusLocation? _currentLocation;
  Timer? _locationTimer;
  bool _isLoading = true;
  String? _error;
  double? _distance;

  @override
  void initState() {
    super.initState();
    _startTracking();
  }

  @override
  void dispose() {
    _stopTracking();
    super.dispose();
  }

  void _startTracking() {
    _fetchLocation();
    _locationTimer = Timer.periodic(const Duration(seconds: 5), (_) {
      _fetchLocation();
    });
  }

  void _stopTracking() {
    _locationTimer?.cancel();
  }

  Future<void> _fetchLocation() async {
    try {
      final response = await ApiService.getBusLocation(widget.bus.busNumber);
      final location = BusLocation.fromJson(response['location']);

      // Calculate distance (simplified - in a real app use geolocator)
      // For now, just show random distance for demonstration
      final distance = 2.5; // km

      setState(() {
        _currentLocation = location;
        _distance = distance;
        _isLoading = false;
        _error = null;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Track Bus'),
        backgroundColor: Colors.blue.shade700,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchLocation,
            tooltip: 'Refresh',
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.error_outline, size: 64, color: Colors.red.shade700),
                      const SizedBox(height: 16),
                      Text(_error!),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _fetchLocation,
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                )
              : SingleChildScrollView(
                  child: Column(
                    children: [
                      // Status Banner
                      Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(20),
                        color: widget.bus.tripActive
                            ? Colors.green.shade700
                            : Colors.grey.shade600,
                        child: Column(
                          children: [
                            Icon(
                              widget.bus.tripActive
                                  ? Icons.directions_bus
                                  : Icons.pause_circle,
                              color: Colors.white,
                              size: 48,
                            ),
                            const SizedBox(height: 8),
                            Text(
                              widget.bus.tripActive ? 'Bus is Active' : 'Bus is Idle',
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ),

                      // Map Placeholder
                      Container(
                        height: 300,
                        color: Colors.grey.shade200,
                        child: Stack(
                          children: [
                            Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(
                                    Icons.map,
                                    size: 80,
                                    color: Colors.grey.shade400,
                                  ),
                                  const SizedBox(height: 16),
                                  Text(
                                    'Map View',
                                    style: TextStyle(
                                      color: Colors.grey.shade600,
                                      fontSize: 18,
                                    ),
                                  ),
                                  const SizedBox(height: 8),
                                  if (_currentLocation != null)
                                    Text(
                                      'Lat: ${_currentLocation!.lat.toStringAsFixed(6)}\n'
                                      'Lng: ${_currentLocation!.lng.toStringAsFixed(6)}',
                                      style: TextStyle(
                                        color: Colors.grey.shade600,
                                        fontSize: 12,
                                      ),
                                      textAlign: TextAlign.center,
                                    ),
                                ],
                              ),
                            ),
                            Positioned(
                              bottom: 16,
                              right: 16,
                              child: Card(
                                child: Padding(
                                  padding: const EdgeInsets.all(8),
                                  child: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      Icon(Icons.update, color: Colors.blue.shade700, size: 16),
                                      const SizedBox(width: 4),
                                      const Text(
                                        'Auto-updates every 5s',
                                        style: TextStyle(fontSize: 12),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),

                      // Location Info
                      Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          children: [
                            // Distance Card
                            Card(
                              elevation: 4,
                              child: Padding(
                                padding: const EdgeInsets.all(20),
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                                  children: [
                                    _buildStatItem(
                                      icon: Icons.straighten,
                                      label: 'Distance',
                                      value: _distance != null
                                          ? '${_distance!.toStringAsFixed(1)} km'
                                          : 'N/A',
                                      color: Colors.blue,
                                    ),
                                    Container(
                                      width: 1,
                                      height: 60,
                                      color: Colors.grey.shade300,
                                    ),
                                    _buildStatItem(
                                      icon: Icons.access_time,
                                      label: 'ETA',
                                      value: _distance != null
                                          ? '${(_distance! * 3).toInt()} min'
                                          : 'N/A',
                                      color: Colors.orange,
                                    ),
                                  ],
                                ),
                              ),
                            ),
                            const SizedBox(height: 16),

                            // Bus Details Card
                            Card(
                              child: Padding(
                                padding: const EdgeInsets.all(16),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Row(
                                      children: [
                                        Icon(Icons.directions_bus, color: Colors.blue.shade700),
                                        const SizedBox(width: 8),
                                        Text(
                                          'Bus Information',
                                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                                fontWeight: FontWeight.bold,
                                              ),
                                        ),
                                      ],
                                    ),
                                    const Divider(height: 24),
                                    _buildInfoRow('Bus Number', widget.bus.busNumber),
                                    _buildInfoRow('Your Boarding Point', widget.student.boardingPoint),
                                    if (widget.route != null)
                                      _buildInfoRow('Route', widget.route!.routeName),
                                    _buildInfoRow(
                                      'Status',
                                      widget.bus.tripActive ? 'On Trip' : 'Idle',
                                      valueColor: widget.bus.tripActive
                                          ? Colors.green
                                          : Colors.grey,
                                    ),
                                  ],
                                ),
                              ),
                            ),
                            const SizedBox(height: 16),

                            // Alert Card
                            if (_distance != null && _distance! < 0.5)
                              Card(
                                color: Colors.orange.shade50,
                                child: Padding(
                                  padding: const EdgeInsets.all(16),
                                  child: Row(
                                    children: [
                                      Icon(Icons.notification_important,
                                          color: Colors.orange.shade700),
                                      const SizedBox(width: 12),
                                      Expanded(
                                        child: Text(
                                          'Bus is approaching your stop!',
                                          style: TextStyle(
                                            color: Colors.orange.shade700,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
    );
  }

  Widget _buildStatItem({
    required IconData icon,
    required String label,
    required String value,
    required Color color,
  }) {
    return Column(
      children: [
        Icon(icon, color: color, size: 32),
        const SizedBox(height: 8),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: Colors.grey.shade600,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  Widget _buildInfoRow(String label, String value, {Color? valueColor}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: TextStyle(color: Colors.grey.shade600),
          ),
          Text(
            value,
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: valueColor ?? Colors.black87,
            ),
          ),
        ],
      ),
    );
  }
}
