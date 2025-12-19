import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'http://10.0.2.2:5000/api';
  
  static String? _sessionCookie;

  // Load session
  static Future<void> _loadSession() async {
    if (_sessionCookie == null) {
      final prefs = await SharedPreferences.getInstance();
      _sessionCookie = prefs.getString('session_cookie');
    }
  }

  // Save session
  static Future<void> _saveSession(String? cookie) async {
    _sessionCookie = cookie;
    final prefs = await SharedPreferences.getInstance();
    if (cookie != null) {
      await prefs.setString('session_cookie', cookie);
    } else {
      await prefs.remove('session_cookie');
    }
  }

  // Login
  static Future<Map<String, dynamic>> login(String driverId, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'user_id': driverId,
          'password': password,
          'user_type': 'driver',
        }),
      );

      if (response.statusCode == 200) {
        final cookie = response.headers['set-cookie'];
        await _saveSession(cookie);
        return jsonDecode(response.body);
      } else {
        throw Exception(jsonDecode(response.body)['error'] ?? 'Login failed');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  // Logout
  static Future<void> logout() async {
    try {
      await _loadSession();
      await http.post(
        Uri.parse('$baseUrl/auth/logout'),
        headers: {
          'Content-Type': 'application/json',
          if (_sessionCookie != null) 'Cookie': _sessionCookie!,
        },
      );
    } finally {
      await _saveSession(null);
    }
  }

  // Get driver data
  static Future<Map<String, dynamic>> getDriver(String driverId) async {
    await _loadSession();
    
    final response = await http.get(
      Uri.parse('$baseUrl/drivers/get/$driverId'),
      headers: {
        'Content-Type': 'application/json',
        if (_sessionCookie != null) 'Cookie': _sessionCookie!,
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch driver data');
    }
  }

  // Get bus data
  static Future<Map<String, dynamic>> getBus(String busNumber) async {
    await _loadSession();
    
    final response = await http.get(
      Uri.parse('$baseUrl/buses/get/$busNumber'),
      headers: {
        'Content-Type': 'application/json',
        if (_sessionCookie != null) 'Cookie': _sessionCookie!,
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch bus data');
    }
  }

  // Get route data
  static Future<Map<String, dynamic>> getRoute(String routeId) async {
    await _loadSession();
    
    final response = await http.get(
      Uri.parse('$baseUrl/routes/get/$routeId'),
      headers: {
        'Content-Type': 'application/json',
        if (_sessionCookie != null) 'Cookie': _sessionCookie!,
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch route data');
    }
  }

  // Get students list
  static Future<Map<String, dynamic>> getStudents() async {
    await _loadSession();
    
    final response = await http.get(
      Uri.parse('$baseUrl/students/list'),
      headers: {
        'Content-Type': 'application/json',
        if (_sessionCookie != null) 'Cookie': _sessionCookie!,
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch students');
    }
  }

  // Start trip
  static Future<Map<String, dynamic>> startTrip(String busNumber) async {
    await _loadSession();
    
    final response = await http.post(
      Uri.parse('$baseUrl/tracking/start-trip/$busNumber'),
      headers: {
        'Content-Type': 'application/json',
        if (_sessionCookie != null) 'Cookie': _sessionCookie!,
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to start trip');
    }
  }

  // End trip
  static Future<Map<String, dynamic>> endTrip(String busNumber) async {
    await _loadSession();
    
    final response = await http.post(
      Uri.parse('$baseUrl/tracking/end-trip/$busNumber'),
      headers: {
        'Content-Type': 'application/json',
        if (_sessionCookie != null) 'Cookie': _sessionCookie!,
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to end trip');
    }
  }

  // Update location
  static Future<void> updateLocation(String busNumber, double lat, double lng) async {
    await _loadSession();
    
    await http.post(
      Uri.parse('$baseUrl/tracking/update-location/$busNumber'),
      headers: {
        'Content-Type': 'application/json',
        if (_sessionCookie != null) 'Cookie': _sessionCookie!,
      },
      body: jsonEncode({
        'lat': lat,
        'lng': lng,
      }),
    );
  }

  // Check authentication
  static Future<bool> isAuthenticated() async {
    await _loadSession();
    return _sessionCookie != null;
  }
}
