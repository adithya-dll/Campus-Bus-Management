"""
Quick validation script to test backend imports and basic configuration
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from config import Config
        print("✓ Config imported")
        
        from utils.database import Database
        print("✓ Database imported")
        
        from utils.validators import validate_email, validate_student_id
        print("✓ Validators imported")
        
        from models.student import Student
        from models.bus import Bus
        from models.route import Route
        from models.driver import Driver
        from models.log import Log
        print("✓ All models imported")
        
        from services.face_service import FaceService
        from services.location_service import LocationService
        from services.notification_service import NotificationService
        print("✓ All services imported")
        
        from routes.auth import auth_bp
        from routes.students import students_bp
        from routes.buses import buses_bp
        from routes.drivers import drivers_bp
        print("✓ All routes imported")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_validators():
    """Test validation functions"""
    print("\nTesting validators...")
    
    from utils.validators import validate_email, validate_student_id, validate_coordinates
    
    # Email validation
    assert validate_email("test@example.com") == True
    assert validate_email("invalid-email") == False
    print("✓ Email validation working")
    
    # Student ID validation
    assert validate_student_id("STU123") == True
    assert validate_student_id("AB") == False  # Too short
    print("✓ Student ID validation working")
    
    # Coordinates validation
    assert validate_coordinates(40.7128, -74.0060) == True
    assert validate_coordinates(200, 100) == False
    print("✓ Coordinates validation working")
    
    print("\n✅ All validators working!")

def test_location_service():
    """Test location service calculations"""
    print("\nTesting location service...")
    
    from services.location_service import LocationService
    
    # Test distance calculation (NYC to LA approximately 4000 km)
    distance = LocationService.calculate_distance(40.7128, -74.0060, 34.0522, -118.2437)
    assert distance > 3900 and distance < 4100
    print(f"✓ Distance calculation working ({distance:.2f} km)")
    
    # Test ETA calculation
    eta = LocationService.calculate_eta(30)  # 30 km
    assert eta['eta_minutes'] == 60  # At 30 km/h
    print(f"✓ ETA calculation working ({eta['eta_formatted']})")
    
    print("\n✅ Location service working!")

if __name__ == '__main__':
    print("=" * 50)
    print("Campus Bus Management System - Backend Validation")
    print("=" * 50)
    
    if test_imports():
        test_validators()
        test_location_service()
        print("\n" + "=" * 50)
        print("✅ Backend validation complete - All tests passed!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ Validation failed - Please fix import errors")
        print("=" * 50)
        sys.exit(1)
