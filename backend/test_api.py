"""
Simple API test script using requests library
"""
import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("API ENDPOINT TESTING")
print("=" * 60)

# Test 1: Health check
print("\n1. Testing health endpoint...")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Root endpoint
print("\n2. Testing root endpoint...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Admin login
print("\n3. Testing admin login...")
try:
    session = requests.Session()
    login_data = {
        "user_id": "admin",
        "password": "admin123",
        "user_type": "admin"
    }
    response = session.post(
        f"{BASE_URL}/api/auth/login",
        json=login_data
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code == 200:
        print("   [OK] Admin login successful!")
        
        # Test 4: Check auth status
        print("\n4. Testing auth check...")
        response = session.get(f"{BASE_URL}/api/auth/check")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test 5: List students (should be empty initially)
        print("\n5. Testing list students...")
        response = session.get(f"{BASE_URL}/api/students/list")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Total students: {data.get('total', 0)}")
        
        # Test 6: List buses
        print("\n6. Testing list buses...")
        response = session.get(f"{BASE_URL}/api/buses/list")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Total buses: {data.get('total', 0)}")
        
        # Test 7: Statistics
        print("\n7. Testing statistics...")
        response = session.get(f"{BASE_URL}/api/logs/statistics")
        print(f"   Status: {response.status_code}")
        data = response.json()
        stats = data.get('system_stats', {})
        print(f"   System Stats:")
        print(f"     - Students: {stats.get('total_students', 0)}")
        print(f"     - Buses: {stats.get('total_buses', 0)}")
        print(f"     - Drivers: {stats.get('total_drivers', 0)}")
        
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
print("API TESTING COMPLETE")
print("=" * 60)
