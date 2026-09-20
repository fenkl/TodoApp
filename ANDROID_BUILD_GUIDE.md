# Android Build Process Guide

## Overview
This document provides detailed instructions for building and packaging the TodoSync application for Android devices.

## Prerequisites

### Android Development Environment
Before building for Android, ensure you have:

1. **Android SDK and NDK** installed
2. **Android Studio** (optional but recommended)
3. **ADB tools** (Android Debug Bridge) 
4. **Java Development Kit (JDK)** version 8 or 11
5. **Rust toolchain** with Android targets

### Setting Up Android Targets for Rust

```bash
# Install Android targets for Rust
rustup target add aarch64-linux-android armv7-linux-androideabi x86_64-linux-android i686-linux-android

# Install cargo-ndk if needed
cargo install cargo-ndk
```

## Build Process

### Step 1: Environment Setup
Ensure all prerequisites are installed and configured. The build process requires a proper Android development environment.

### Step 2: Running the Build Script
From the root project directory:

```bash
# Make script executable (run once)
chmod +x build.sh

# Execute the build process  
./build.sh
```

The build script will:
1. Build frontend assets using npm
2. Prepare Android build environment 
3. Generate self-signed APK file

### Step 3: Generated Output Files
After successful build, the following files will be created in `build-android/` directory:

- `todo-sync.apk` - Debug version
- `todo-sync-release.apk` - Release version (if properly signed)

## Installation on Android Device

### Method 1: Using ADB
```bash
# Install directly from computer to connected device 
adb install build-android/todo-sync.apk
```

### Method 2: Manual Installation  
1. Transfer the APK file to your Android device
2. Enable "Install from unknown sources" in device settings
3. Tap on the APK file to install

## Development Workflow

### Quick Test Cycle
```bash
# For development testing on Android device
npm run tauri android dev
```

### Release Build
```bash
# For generating release APK 
npm run tauri android build --release
```

## Important Notes

### Security
- The debug APK will use a self-signed certificate
- For production releases, proper certificate signing should be implemented

### Device Compatibility
The application is configured to work on:
- Android 7.0 (API level 24) and above
- Supports various screen sizes and resolutions

### Permissions
The application requires the following permissions in `AndroidManifest.xml`:
- Network access (for WebSocket connections)
- Internet access  
- Storage access (for local data storage)

## Troubleshooting

### Common Issues

1. **"No such file or directory" errors during build**:
   - Ensure all dependencies are properly installed
   - Check that the Android SDK path is correctly configured

2. **Rust compilation problems**:
   - Make sure Rust targets are added for Android (`rustup target add`)

3. **APK generation fails**:
   - Check that Tauri can find the correct Android build tools  
   - Verify that Node.js and npm are functional

4. **Signature errors**:
   - Debug APKs are self-signed with default keys
   - Release builds require proper certificate setup

### Debugging Steps
1. Run `npm run tauri android dev` to test on device
2. Check logs with `adb logcat | grep todo`
3. Verify Android development environment with `android --version`

## Build Customization

The Tauri configuration in `tauri.conf.json` can be modified for custom Android settings:

```json
{
  "tauri": {
    "bundle": {
      "identifier": "com.todosync.app",
      "targets": ["android"],
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png"
      ]
    }
  }
}
```

## Testing Strategy

### Device Testing
- Test on different Android versions (7.0-14)
- Verify offline queue functionality on mobile
- Check WebSocket connection robustness 
- Validate conflict resolution on mobile devices

### Performance Testing
- Monitor memory usage on low-end devices  
- Test with multiple concurrent connections
- Verify app responsiveness during sync operations

## Release Process

For production releases, follow these steps:

1. Generate release key using `keytool`
2. Configure appropriate signing information in build scripts
3. Run release build: `npm run tauri android build --release` 
4. Test on multiple devices before distribution

This completes the Android build process documentation for the TodoSync application.