import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // Use 10.0.2.2 for Android emulator to access localhost
  static const String baseUrl = 'http://10.0.2.2:5000/api';
  
  static String? _sessionCookie;

  // Get session cookie from storage
  static Future<void> _loadSession() async {
    if (_sessionCookie == null) {
      final prefs = await SharedPreferences.getInstance();
      _sessionCookie = prefs.getString('session_cookie');
    }
  }

  // Save session cookie
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
  static Future<Map<String, dynamic>> login(String rollNumber, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'user_id': rollNumber,  // Backend expects user_id
          'password': password,
          'user_type': 'student',
        }),
      );

      if (response.statusCode == 200) {
        // Extract and save session cookie
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

  // Get student data
  static Future<Map<String, dynamic>> getStudent(String rollNumber) async {
    await _loadSession();
    
    final response = await http.get(
      Uri.parse('$baseUrl/students/get/$rollNumber'),
      headers: {
        'Content-Type': 'application/json',
        if (_sessionCookie != null) 'Cookie': _sessionCookie!,
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else if (response.statusCode == 401) {
      await _saveSession(null);
      throw Exception('Unauthorized - please login again');
    } else {
      throw Exception('Failed to fetch student data');
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

  // Get bus location
  static Future<Map<String, dynamic>> getBusLocation(String busNumber) async {
    await _loadSession();
    
    final response = await http.get(
      Uri.parse('$baseUrl/tracking/get-location/$busNumber'),
      headers: {
        'Content-Type': 'application/json',
        if (_sessionCookie != null) 'Cookie': _sessionCookie!,
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch bus location');
    }
  }

  // Check authentication
  static Future<bool> isAuthenticated() async {
    await _loadSession();
    return _sessionCookie != null;
  }
}
