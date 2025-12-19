"""
Full backend validation with face_recognition and MongoDB
"""
import sys

print("=" * 60)
print("FULL BACKEND VALIDATION - With Face Recognition + MongoDB")
print("=" * 60)

# Test 1: Face recognition import
print("\n1. Testing face_recognition import...")
try:
    import face_recognition
    import dlib
    print("   [OK] face_recognition library")
    print(f"   [OK] dlib version: {dlib.__version__}")
    print(f"   [OK] face_recognition available")
except ImportError as e:
    print(f"   [FAILED] {e}")
    sys.exit(1)

# Test 2: All core imports
print("\n2. Testing all imports...")
try:
    from config import Config
    from utils.database import Database
    from models.student import Student
    from models.bus import Bus
    from services.face_service import FaceService
    from services.location_service import LocationService
    from routes.auth import auth_bp
    from routes.students import students_bp
    from routes.face_recognition import face_bp
    print("   [OK] All imports successful")
except ImportError as e:
    print(f"   [FAILED] {e}")
    sys.exit(1)

# Test 3: MongoDB connection
print("\n3. Testing MongoDB connection...")
try:
    success = Database.initialize()
    if success:
        print("   [OK] MongoDB connected successfully")
        db = Database.get_db()
        print(f"   [OK] Database: {Config.DATABASE_NAME}")
    else:
        print("   [FAILED] MongoDB connection failed")
        print("   Make sure MongoDB is running (mongod)")
        sys.exit(1)
except Exception as e:
    print(f"   [FAILED] {e}")
    print("   Make sure MongoDB is running")
    sys.exit(1)

# Test 4: Flask app creation
print("\n4. Testing Flask app...")
try:
    from app import create_app
    app = create_app()
    print("   [OK] Flask app created")
    print(f"   [OK] Debug mode: {app.config['DEBUG']}")
except Exception as e:
    print(f"   [FAILED] {e}")
    sys.exit(1)

# Test 5: Face recognition functionality
print("\n5. Testing face recognition...")
try:
    # Check if face service is available
    from services.face_service import FACE_RECOGNITION_AVAILABLE
    if FACE_RECOGNITION_AVAILABLE:
        print("   [OK] Face recognition service available")
    else:
        print("   [WARNING] Face recognition not available")
except Exception as e:
    print(f"   [NOTE] {e}")

print("\n" + "=" * 60)
print("VALIDATION COMPLETE - Backend Ready!")
print("=" * 60)
print("\nBackend is ready to run. Start with:")
print("  python app.py")
print("\nThen test APIs:")
print("  http://localhost:5000/health")
print("  http://localhost:5000/api/auth/login")
