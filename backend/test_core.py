"""
Test basic backend functionality without face_recognition
"""
import sys

print("Testing Core Backend Components (without face_recognition)")
print("=" * 60)

# Test 1: Basic imports
print("\n1. Testing imports...")
try:
    from config import Config
    print("   [OK] Config")
    
    from utils.validators import validate_email, validate_student_id, validate_coordinates
    print("   [OK] Validators")
    
    from models.student import Student
    from models.bus import Bus
    from models.route import Route
    from models.driver import Driver
    from models.log import Log
    print("   [OK] All models")
    
    from services.location_service import LocationService
    from services.notification_service import NotificationService
    print("   [OK] Location and Notification services")
    
    print("   (Skipping face_service - requires dlib/CMake)")
    
    from routes.auth import auth_bp
    from routes.students import students_bp
    from routes.buses import buses_bp
    print("   [OK] Core routes")
    
    print("\n   SUCCESS: All core imports working!")
    
except ImportError as e:
    print(f"\n   FAILED: {e}")
    sys.exit(1)

# Test 2: Validators
print("\n2. Testing validators...")
try:
    assert validate_email("test@example.com") == True
    assert validate_email("invalid") == False
    print("   [OK] Email validation")
    
    assert validate_student_id("STU123") == True
    assert validate_student_id("AB") == False
    print("   [OK] Student ID validation")
    
    assert validate_coordinates(40.7128, -74.0060) == True
    assert validate_coordinates(200, 100) == False
    print("   [OK] GPS validation")
    
    print("\n   SUCCESS: All validators working!")
except AssertionError as e:
    print(f"\n   FAILED: Validation error {e}")
    sys.exit(1)

# Test 3: Location Service
print("\n3. Testing location calculations...")
try:
    # NYC to LA distance
    distance = LocationService.calculate_distance(40.7128, -74.0060, 34.0522, -118.2437)
    assert 3900 < distance < 4100
    print(f"   [OK] Distance NYC->LA: {distance:.2f} km")
    
    # ETA calculation
    eta = LocationService.calculate_eta(30)
    assert eta['eta_minutes'] == 60
    print(f"   [OK] ETA for 30km @ 30km/h: {eta['eta_formatted']}")
    
    # Geofencing
    near = LocationService.is_near_stop(40.7128, -74.0060, 40.7130, -74.0062, threshold_km=0.5)
    assert near == True
    print(f"   [OK] Geofencing check")
    
    print("\n   SUCCESS: Location service working!")
except Exception as e:
    print(f"\n   FAILED: {e}")
    sys.exit(1)

# Test 4: Flask app creation
print("\n4. Testing Flask app initialization...")
try:
    # Note: This will fail if MongoDB is not running, which is expected
    from app import create_app
    print("   [OK] Flask app can be imported")
    print("   (Database connection will be tested when MongoDB is running)")
    
except Exception as e:
    print(f"   Note: {e}")

print("\n" + "=" * 60)
print("CORE BACKEND VALIDATION COMPLETE!")
print("=" * 60)
print("\nNext steps:")
print("1. Install MongoDB (or use MongoDB Atlas)")
print("2. For face recognition, install CMake from cmake.org")
print("3. Then run: pip install face-recognition")
print("4. Start the server: python app.py")
