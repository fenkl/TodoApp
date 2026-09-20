# TodoSync Build and Package Generation Guide

## Overview
This document provides comprehensive instructions for building and packaging the TodoSync application across different platforms and target devices.

## Build Environment Requirements

### General Prerequisites
- Node.js and npm installed (for frontend builds)
- Rust toolchain installed (for Tauri builds)
- Python 3.8+ (for backend server)
- Android SDK and NDK (for Android builds)

### Platform-Specific Dependencies

#### Linux (Manjaro/Ubuntu)
```bash
# For building AppImage and RPM packages on Manjaro
sudo pacman -S webkit2gtk-4.1 librsvg libayatana-appindicator rust

# For Ubuntu/Debian-based systems
sudo apt install libwebkit2gtk-4.1-dev librsvg2-dev libappindicator3-dev rustc
```

#### Windows
- Visual Studio Build Tools or Visual Studio Community 2022
- Windows SDK
- Rust toolchain

#### macOS
- Xcode Command Line Tools
- Rust toolchain

## Directory Structure for Builds

The project has the following structure relevant to building:
```
.
├── backend/              # Backend server code (Python/FastAPI)
│   ├── main.py           # Main server entry point  
│   ├── db.py             # Database handling
│   ├── conflict_handler.py  # Conflict resolution logic
│   └── install.sh        # Raspberry Pi installation script
├── frontend/             # Frontend code (Svelte/Vue with Tauri)
│   ├── src-tauri/        # Tauri Rust code
│   │   ├── Cargo.toml    # Rust dependencies
│   │   └── src/main.rs   # Main Tauri entry point
│   ├── src/              # Svelte components
│   └── package.json      # Frontend dependencies and scripts
├── build.sh              # Android APK build script
├── tauri.conf.json       # Tauri configuration for all targets
└── package.json          # Frontend build configuration
```

## Build Process by Target Platform

### 1. Desktop Applications (Linux, Windows, macOS)

All desktop builds are performed from the root project directory.

#### Linux Package Generation
```bash
# Run from root project directory
npm run tauri build
```

This command will generate:
- **AppImage** file for distribution (e.g., `todo-sync-x86_64.AppImage`)
- **RPM package** for Red Hat-based distributions (e.g., `todo-sync-x86_64.rpm`)

The build process automatically detects the platform and creates appropriate packages.

#### Windows/MacOS Package Generation
```bash
# Run from root project directory  
npm run tauri build
```

This command will generate:
- Windows executable (.exe)
- macOS application bundle (.app)
- Additional platform-specific packages

### 2. Android Application

Android builds are performed from the **root project directory** using the custom script.

#### Building Android APK
```bash
# Make the script executable (run once)
chmod +x build.sh

# Run the build process
./build.sh
```

This will:
1. Build frontend assets with npm
2. Prepare Android build environment
3. Generate self-signed APK file in `build-android/` directory

#### Installing to Android Device
```bash
# After building the APK
adb install build-android/todo-sync.apk  # or similar path
```

The Android package will be created at:
- `build-android/todo-sync.apk` (debug version)
- `build-android/todo-sync-release.apk` (release version with proper signing keys)

## Backend Server Setup

### Raspberry Pi Installation
For autonomous operation on a Raspberry Pi, use the installation script in the backend directory:

```bash
# From root project directory
chmod +x backend/install.sh
./backend/install.sh
```

This script provides step-by-step guidance for:
- System package updates
- Python environment setup
- Virtual environment creation
- Dependency installation from requirements.txt
- Systemd service configuration for auto-startup  

### Running Backend Server
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if created during install)
# Run the server on port 8000
python main.py
```

The backend server will be available at: `http://192.168.2.2:8000`

## Environment Variables and Configuration

### Tauri Configuration
The `tauri.conf.json` file configures:
- Product name: "TodoSync"
- Version: "0.1.0"
- Window size: 800x600 for desktop versions
- Bundle targets: AppImage, RPM (Linux), Windows, macOS, Android
- Bundle identifier: "com.todosync.app"

### Frontend Configuration  
The `package.json` defines:
- Build scripts for development and production
- Dependencies including Tauri framework
- Svelte frontend components

## Testing Before Packaging

Before building packages, run all tests to ensure functionality:

```bash
# Run backend tests
cd backend
python -m pytest tests/ -v

# Run frontend tests  
cd ../frontend  
npm run test  # or appropriate test command for project

# Run full integration tests
cd ..
python smoke_test.py
```

## Package Location and File Names

### Desktop Packages (Generated in root directory)
- **Linux**: 
  - AppImage: `todo-sync-x86_64.AppImage`
  - RPM: `todo-sync-x86_64.rpm`
- **Windows**: 
  - Executable: `todo-sync.exe`
- **macOS**:  
  - Application bundle: `TodoSync.app`

### Android Package
- Generated in: `build-android/` directory
- File name: `todo-sync.apk` or similar pattern

## Device-Specific Usage

### Desktop Devices (Windows, macOS, Linux)
These devices use the desktop application packages:
- Install AppImage on Linux with proper execution permissions  
- Install .exe on Windows
- Install .app on macOS

### Android Devices
Android devices use the APK package generated by the build script.

## Troubleshooting Build Issues

### Common Build Errors and Solutions

1. **"Command not found: tauri"**:
   - Solution: Install Tauri CLI with `npm install -g @tauri-apps/cli`

2. **Rust compilation errors**:  
   - Solution: Ensure Rust toolchain is up to date with `rustup update`

3. **Missing Android SDK/NDK**:
   - Solution: Install required Android Development tools

4. **Node.js/npm not found**:
   - Solution: Install Node.js from nodejs.org or package manager  

5. **Permission denied for build files**:
   - Solution: Set proper permissions with `chmod +x` on scripts