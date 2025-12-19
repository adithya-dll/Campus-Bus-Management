import 'dart:async';
import 'package:geolocator/geolocator.dart';
import 'api_service.dart';

class LocationService {
  Timer? _locationTimer;
  bool _isTracking = false;

  bool get isTracking => _isTracking;

  Future<void> startTracking(String busNumber) async {
    if (_isTracking) return;

    _isTracking = true;

    // Update location every 10 seconds
    _locationTimer = Timer.periodic(const Duration(seconds: 10), (timer) async {
      try {
        final position = await getCurrentLocation();
        await ApiService.updateLocation(
          busNumber,
          position.latitude,
          position.longitude,
        );
      } catch (e) {
        print('Error updating location: $e');
      }
    });

    // Send initial location immediately
    try {
      final position = await getCurrentLocation();
      await ApiService.updateLocation(
        busNumber,
        position.latitude,
        position.longitude,
      );
    } catch (e) {
      print('Error sending initial location: $e');
    }
  }

  void stopTracking() {
    _locationTimer?.cancel();
    _locationTimer = null;
    _isTracking = false;
  }

  Future<Position> getCurrentLocation() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      throw Exception('Location services are disabled');
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        throw Exception('Location permissions are denied');
      }
    }

    if (permission == LocationPermission.deniedForever) {
      throw Exception('Location permissions are permanently denied');
    }

    return await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.high,
    );
  }
}
