# Student Mobile App

Campus Bus Management System - Student Mobile Application

## Features

- 🔐 **Login** - Authenticate with roll number
- 📱 **Digital Bus Pass** - QR code for easy verification  
- 📍 **Real-time Tracking** - Track your bus location live
- 🗺️ **Route Information** - View all boarding points and schedules
- 🔔 **Notifications** - Get notified when bus is approaching

## Tech Stack

- **Flutter 3.x**
- **HTTP** for API communication
- **Provider** for state management
- **QR Flutter** for QR code generation
- **Google Maps Flutter** for tracking (ready for integration)

## Setup

### Prerequisites
- Flutter SDK 3.0 or higher
- Android Studio / VS Code with Flutter extensions
- Android device or emulator

### Installation

1. **Install dependencies**
```bash
flutter pub get
```

2. **Configure backend URL**

Edit `lib/services/api_service.dart` and update the base URL:
- For Android emulator: `http://10.0.2.2:5000/api`
- For physical device: `http://<your-pc-ip>:5000/api`

3. **Run the app**
```bash
# For Android
flutter run

# For specific device
flutter devices
flutter run -d <device-id>
```

## App Structure

```
lib/
├── main.dart                  # App entry point
├── models/
│   ├── student.dart           # Student data model
│   ├── bus.dart               # Bus & location models
│   └── route.dart             # Route model
├── services/
│   └── api_service.dart       # Backend API integration
└── screens/
    ├── login_screen.dart      # Login page
    ├── home_screen.dart       # Dashboard
    ├── bus_pass_screen.dart   # QR code pass
    ├── tracking_screen.dart   # Live bus tracking
    └── schedule_screen.dart   # Route schedule
```

## Usage

### Login
1. Enter your roll number (e.g., R2024001)
2. Password is optional (uses roll number if empty)
3. Tap Login

### View Bus Pass
- Shows your QR code
- Display student and bus details
- Present QR to driver when boarding

### Track Bus
- Real-time location updates every 5 seconds
- Shows distance and ETA to your boarding point
- Alerts when bus is nearby

### View Schedule
- See all boarding points on your route
- Your boarding point is highlighted
- View route distance and duration

## Backend Integration

The app connects to the Flask backend API:

**Endpoints Used:**
- `POST /api/auth/login` - Student authentication
- `GET /api/students/get/<roll_number>` - Student data
- `GET /api/buses/get/<bus_number>` - Bus information
- `GET /api/routes/get/<route_id>` - Route details
- `GET /api/tracking/get-location/<bus_number>` - Real-time location

## Development

### Adding Google Maps

To enable real Google Maps:

1. Get API key from Google Cloud Console
2. Add to `android/app/src/main/AndroidManifest.xml`:
```xml
<meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_API_KEY_HERE"/>
```

3. Update `TrackingScreen` to use `GoogleMap` widget

### Push Notifications

Configured with `flutter_local_notifications`. Ready for:
- Bus arrival alerts
- Route changes
- Schedule updates

## Building

### Debug APK
```bash
flutter build apk --debug
```

### Release APK
```bash
flutter build apk --release
```

APK will be in `build/app/outputs/flutter-apk/`

## Testing

Make sure backend is running:
```bash
cd ../backend
python app.py
```

Test with a student account created in the admin panel.

## License

Part of Campus Bus Management System
