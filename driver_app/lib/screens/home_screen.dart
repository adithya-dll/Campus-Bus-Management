import 'package:flutter/material.dart';
import '../models/driver.dart';
import '../models/bus.dart';
import '../models/route.dart';
import '../services/api_service.dart';
import '../services/location_service.dart';

class HomeScreen extends StatefulWidget {
  final String driverId;

  const HomeScreen({super.key, required this.driverId});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Driver? _driver;
  Bus? _bus;
  BusRoute? _route;
  bool _isLoading = true;
  String? _error;
  final LocationService _locationService = LocationService();

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final driverResponse = await ApiService.getDriver(widget.driverId);
      final driver = Driver.fromJson(driverResponse['driver']);
      
      Bus? bus;
      BusRoute? route;

      if (driver.assignedBus.isNotEmpty) {
        try {
          final busResponse = await ApiService.getBus(driver.assignedBus);
          bus = Bus.fromJson(busResponse['bus']);

          if (bus.routeId != null && bus.routeId!.isNotEmpty) {
            final routeResponse = await ApiService.getRoute(bus.routeId!);
            route = BusRoute.fromJson(routeResponse['route']);
          }
        } catch (e) {
          print('Error fetching bus/route: $e');
        }
      }

      setState(() {
        _driver = driver;
        _bus = bus;
        _route = route;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  Future<void> _toggleTrip() async {
    if (_bus == null) return;

    try {
      if (_bus!.tripActive) {
        await ApiService.endTrip(_bus!.busNumber);
        _locationService.stopTracking();
      } else {
        await ApiService.startTrip(_bus!.busNumber);
        await _locationService.startTracking(_bus!.busNumber);
      }
      await _loadData();
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  Future<void> _handleLogout() async {
    await ApiService.logout();
    _locationService.stopTracking();
    if (mounted) {
      Navigator.of(context).pushReplacementNamed('/login');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Driver Portal'),
        backgroundColor: Colors.green.shade700,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _handleLogout,
            tooltip: 'Logout',
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
                        onPressed: _loadData,
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                )
              : RefreshIndicator(
                  onRefresh: _loadData,
                  child: SingleChildScrollView(
                    physics: const AlwaysScrollableScrollPhysics(),
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Driver Info Card
                        Card(
                          elevation: 4,
                          child: Padding(
                            padding: const EdgeInsets.all(20),
                            child: Row(
                              children: [
                                CircleAvatar(
                                  radius: 30,
                                  backgroundColor: Colors.green.shade100,
                                  child: Icon(
                                    Icons.person,
                                    size: 40,
                                    color: Colors.green.shade700,
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'Driver ${_driver!.name}',
                                        style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                                              fontWeight: FontWeight.bold,
                                            ),
                                      ),
                                      Text(
                                        _driver!.driverId,
                                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                              color: Colors.grey.shade600,
                                            ),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),

                        // Trip Status
                        if (_bus != null)
                          Card(
                            color: _bus!.tripActive
                                ? Colors.green.shade50
                                : Colors.grey.shade200,
                            child: Padding(
                              padding: const EdgeInsets.all(16),
                              child: Row(
                                children: [
                                  Icon(
                                    _bus!.tripActive ? Icons.check_circle : Icons.pause_circle,
                                    color: _bus!.tripActive
                                        ? Colors.green.shade700
                                        : Colors.grey.shade600,
                                  ),
                                  const SizedBox(width: 12),
                                  Text(
                                    _bus!.tripActive ? 'Trip Active' : 'Trip Idle',
                                    style: TextStyle(
                                      fontWeight: FontWeight.bold,
                                      color: _bus!.tripActive
                                          ? Colors.green.shade700
                                          : Colors.grey.shade600,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        const SizedBox(height: 16),

                        // Bus Info
                        if (_bus != null && _route != null)
                          Card(
                            elevation: 4,
                            child: Padding(
                              padding: const EdgeInsets.all(16),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      Icon(Icons.directions_bus, color: Colors.green.shade700),
                                      const SizedBox(width: 8),
                                      Text(
                                        'Bus Information',
                                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                              fontWeight: FontWeight.bold,
                                            ),
                                      ),
                                    ],
                                  ),
                                  const Divider(height: 24),
                                  _buildInfoRow('Bus Number', _bus!.busNumber),
                                  _buildInfoRow('Route', _route!.routeName),
                                  _buildInfoRow('Capacity', '${_bus!.capacity} seats'),
                                ],
                              ),
                            ),
                          ),
                        const SizedBox(height: 24),

                        // Trip Control Button
                        if (_bus != null)
                          SizedBox(
                            width: double.infinity,
                            height: 70,
                            child: ElevatedButton(
                              onPressed: _toggleTrip,
                              style: ElevatedButton.styleFrom(
                                backgroundColor: _bus!.tripActive
                                    ? Colors.red.shade700
                                    : Colors.green.shade700,
                                foregroundColor: Colors.white,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(12),
                                ),
                              ),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(
                                    _bus!.tripActive ? Icons.stop : Icons.play_arrow,
                                    size: 36,
                                  ),
                                  const SizedBox(width: 12),
                                  Text(
                                    _bus!.tripActive ? 'END TRIP' : 'START TRIP',
                                    style: const TextStyle(
                                      fontSize: 24,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        const SizedBox(height: 16),

                        // Quick Actions
                        Text(
                          'Quick Actions',
                          style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                fontWeight: FontWeight.bold,
                              ),
                        ),
                        const SizedBox(height: 16),

                        GridView.count(
                          crossAxisCount: 2,
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          mainAxisSpacing: 16,
                          crossAxisSpacing: 16,
                          children: [
                            _buildActionCard(
                              context,
                              icon: Icons.qr_code_scanner,
                              title: 'Scan Pass',
                              subtitle: 'QR Code',
                              color: Colors.blue,
                              onTap: () => Navigator.pushNamed(context, '/scanner'),
                            ),
                            _buildActionCard(
                              context,
                              icon: Icons.people,
                              title: 'Students',
                              subtitle: 'View List',
                              color: Colors.orange,
                              onTap: () => Navigator.pushNamed(context, '/students', arguments: _bus?.busNumber),
                            ),
                            _buildActionCard(
                              context,
                              icon: Icons.warning,
                              title: 'Emergency',
                              subtitle: 'Alert',
                              color: Colors.red,
                              onTap: () => showDialog(
                                context: context,
                                builder: (context) => AlertDialog(
                                  title: const Text('Emergency Alert'),
                                  content: const Text('Emergency feature coming soon!'),
                                  actions: [
                                    TextButton(
                                      onPressed: () => Navigator.pop(context),
                                      child: const Text('OK'),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                            _buildActionCard(
                              context,
                              icon: Icons.refresh,
                              title: 'Refresh',
                              subtitle: 'Update Data',
                              color: Colors.green,
                              onTap: _loadData,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
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
            style: const TextStyle(
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String subtitle,
    required Color color,
    VoidCallback? onTap,
  }) {
    return Card(
      elevation: 4,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                icon,
                size: 48,
                color: color,
              ),
              const SizedBox(height: 12),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 4),
              Text(
                subtitle,
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey.shade600,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _locationService.stopTracking();
    super.dispose();
  }
}
