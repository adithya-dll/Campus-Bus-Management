# Campus Bus Management System Backend

Flask-based REST API for managing campus transportation with face recognition and real-time tracking.

## Features

- 🔐 Session-based authentication (students, drivers, admins)
- 👤 Student management with face recognition
- 🚌 Bus fleet management
- 🗺️ Real-time GPS tracking
- 📸 Face verification for bus entry
- 📊 Analytics and reporting
- 🚨 Security alerts and logging

## Tech Stack

- **Framework**: Flask 3.0
- **Database**: MongoDB
- **Face Recognition**: face_recognition (dlib)
- **Image Processing**: OpenCV, Pillow

## Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB (local or Atlas)
- C++ build tools (for dlib compilation)

### Installation

1. **Clone and navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example env file
copy .env.example .env

# Edit .env with your settings
# MONGODB_URI=mongodb://localhost:27017/
# SECRET_KEY=your-secret-key
```

5. **Run the application**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Documentation

### Authentication

- `POST /api/auth/login` - Login (student/driver/admin)
- `POST /api/auth/logout` - Logout
- `GET /api/auth/check` - Check auth status

### Students

- `POST /api/students/add` - Add student (admin)
- `PUT /api/students/update/<id>` - Update student (admin)
- `GET /api/students/get/<id>` - Get student
- `GET /api/students/list` - List students (admin)
- `DELETE /api/students/delete/<id>` - Delete student (admin)
- `POST /api/students/register-face/<id>` - Register face (admin)

### Buses

- `POST /api/buses/create` - Create bus (admin)
- `PUT /api/buses/update/<id>` - Update bus (admin)
- `GET /api/buses/get/<id>` - Get bus
- `GET /api/buses/list` - List buses
- `DELETE /api/buses/delete/<id>` - Delete bus (admin)
- `PUT /api/buses/assign-driver/<id>` - Assign driver (admin)
- `PUT /api/buses/assign-route/<id>` - Assign route (admin)

### Tracking

- `POST /api/tracking/update-location` - Update bus location (driver)
- `GET /api/tracking/get-location/<bus_id>` - Get bus location
- `GET /api/tracking/get-all-locations` - Get all active bus locations
- `POST /api/tracking/start-trip/<bus_id>` - Start trip (driver)
- `POST /api/tracking/end-trip/<bus_id>` - End trip (driver)

### Face Recognition

- `POST /api/face/verify` - Verify student face (driver)
- `POST /api/face/detect` - Detect faces in frame (driver)

### Logs

- `GET /api/logs/entry` - Get entry logs
- `GET /api/logs/alerts` - Get alerts
- `PUT /api/logs/alerts/resolve/<id>` - Resolve alert (admin)
- `GET /api/logs/statistics` - Get statistics (admin)
- `POST /api/logs/create-alert` - Create alert (driver/admin)

## Project Structure

```
backend/
├── app.py                  # Main Flask application
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
│
├── models/               # Data models
│   ├── student.py
│   ├── bus.py
│   ├── route.py
│   ├── driver.py
│   └── log.py
│
├── routes/               # API routes
│   ├── auth.py
│   ├── students.py
│   ├── buses.py
│   ├── routes.py
│   ├── drivers.py
│   ├── tracking.py
│   ├── face_recognition.py
│   └── logs.py
│
├── services/             # Business logic
│   ├── face_service.py
│   ├── location_service.py
│   └── notification_service.py
│
├── utils/                # Utilities
│   ├── database.py
│   └── validators.py
│
└── uploads/              # Face images (created automatically)
    └── faces/
```

## Default Credentials

**Admin Login:**
- User ID: `admin`
- Password: `admin123`

**Note:** Change these credentials in production!

## Development

### Running in Development Mode

```bash
# With auto-reload
python app.py
```

### Using Production Server

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## MongoDB Schema

See `models/` directory for detailed schema definitions.

## Security Notes

- 🔴 Currently using plain text passwords (implement bcrypt hashing for production)
- 🔴 Session-based auth (consider JWT for mobile apps)
- 🟢 Input validation and sanitization implemented
- 🟢 CORS configured for specific origins
- 🟢 Request body size limits enforced

## Face Recognition

- **Model**: HOG (configurable to CNN for better accuracy)
- **Tolerance**: 0.6 (configurable, lower = stricter)
- **Supported formats**: JPG, JPEG, PNG
- **Max file size**: 16MB

## License

Proprietary - Campus Bus Management System
