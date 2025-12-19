import 'package:flutter/material.dart';
import '../models/student.dart';
import '../models/bus.dart';
import '../models/route.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  final String rollNumber;

  const HomeScreen({super.key, required this.rollNumber});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Student? _student;
  Bus? _bus;
  BusRoute? _route;
  bool _isLoading = true;
  String? _error;

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
      // Fetch student data
      final studentResponse = await ApiService.getStudent(widget.rollNumber);
      final student = Student.fromJson(studentResponse['student']);
      
      Bus? bus;
      BusRoute? route;

      // Fetch bus data if assigned
      if (student.assignedBus.isNotEmpty) {
        try {
          final busResponse = await ApiService.getBus(student.assignedBus);
          bus = Bus.fromJson(busResponse['bus']);

          // Fetch route data if bus has a route
          if (bus.routeId != null && bus.routeId!.isNotEmpty) {
            final routeResponse = await ApiService.getRoute(bus.routeId!);
            route = BusRoute.fromJson(routeResponse['route']);
          }
        } catch (e) {
          // Bus or route data might not be available
          print('Error fetching bus/route: $e');
        }
      }

      setState(() {
        _student = student;
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

  Future<void> _handleLogout() async {
    await ApiService.logout();
    if (mounted) {
      Navigator.of(context).pushReplacementNamed('/login');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Campus Bus App'),
        backgroundColor: Colors.purple.shade700,
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
                      Text(
                        'Error loading data',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      const SizedBox(height: 8),
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
                        // Welcome Card
                        Card(
                          elevation: 4,
                          child: Padding(
                            padding: const EdgeInsets.all(20),
                            child: Row(
                              children: [
                                CircleAvatar(
                                  radius: 30,
                                  backgroundColor: Colors.purple.shade100,
                                  child: Icon(
                                    Icons.person,
                                    size: 40,
                                    color: Colors.purple.shade700,
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'Welcome,',
                                        style: Theme.of(context).textTheme.bodyMedium,
                                      ),
                                      Text(
                                        _student!.name,
                                        style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                                              fontWeight: FontWeight.bold,
                                            ),
                                      ),
                                      Text(
                                        _student!.rollNumber,
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

                        // Bus Pass Validity
                        Card(
                          color: _student!.busPassValid
                              ? Colors.green.shade50
                              : Colors.red.shade50,
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Row(
                              children: [
                                Icon(
                                  _student!.busPassValid ? Icons.check_circle : Icons.warning,
                                  color: _student!.busPassValid
                                      ? Colors.green.shade700
                                      : Colors.red.shade700,
                                ),
                                const SizedBox(width: 12),
                                Text(
                                  _student!.busPassValid
                                      ? 'Bus Pass is Valid'
                                      : 'Bus Pass is Invalid',
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    color: _student!.busPassValid
                                        ? Colors.green.shade700
                                        : Colors.red.shade700,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),

                        // Bus Info Card
                        if (_bus != null && _route != null) ...[
                          Card(
                            elevation: 4,
                            child: Padding(
                              padding: const EdgeInsets.all(16),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      Icon(Icons.directions_bus, color: Colors.purple.shade700),
                                      const SizedBox(width: 8),
                                      Text(
                                        'Your Bus Information',
                                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                              fontWeight: FontWeight.bold,
                                            ),
                                      ),
                                    ],
                                  ),
                                  const Divider(height: 24),
                                  _buildInfoRow('Bus Number', _bus!.busNumber),
                                  _buildInfoRow('Route', _route!.routeName),
                                  _buildInfoRow('Your Boarding Point', _student!.boardingPoint),
                                  _buildInfoRow(
                                    'Status',
                                    _bus!.tripActive ? 'On Trip' : 'Idle',
                                    valueColor: _bus!.tripActive ? Colors.green : Colors.grey,
                                  ),
                                ],
                              ),
                            ),
                          ),
                          const SizedBox(height: 24),
                        ],

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
                              icon: Icons.qr_code,
                              title: 'Bus Pass',
                              subtitle: 'View QR Code',
                              color: Colors.purple,
                              onTap: () => Navigator.pushNamed(context, '/bus-pass', arguments: _student),
                            ),
                            _buildActionCard(
                              context,
                              icon: Icons.location_on,
                              title: 'Track Bus',
                              subtitle: 'Live Location',
                              color: Colors.blue,
                              onTap: _bus != null
                                  ? () => Navigator.pushNamed(
                                        context,
                                        '/tracking',
                                        arguments: {
                                          'bus': _bus,
                                          'student': _student,
                                          'route': _route,
                                        },
                                      )
                                  : null,
                            ),
                            _buildActionCard(
                              context,
                              icon: Icons.schedule,
                              title: 'Schedule',
                              subtitle: 'View Route',
                              color: Colors.orange,
                              onTap: _route != null
                                  ? () => Navigator.pushNamed(
                                        context,
                                        '/schedule',
                                        arguments: {
                                          'route': _route,
                                          'student': _student,
                                        },
                                      )
                                  : null,
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

  Widget _buildActionCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String subtitle,
    required Color color,
    VoidCallback? onTap,
  }) {
    final isDisabled = onTap == null;

    return Card(
      elevation: isDisabled ? 1 : 4,
      color: isDisabled ? Colors.grey.shade200 : null,
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
                color: isDisabled ? Colors.grey.shade400 : color,
              ),
              const SizedBox(height: 12),
              Text(
                title,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: isDisabled ? Colors.grey.shade600 : Colors.black87,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 4),
              Text(
                subtitle,
                style: TextStyle(
                  fontSize: 12,
                  color: isDisabled ? Colors.grey.shade500 : Colors.grey.shade600,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
