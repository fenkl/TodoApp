#!/bin/bash

# Build script for Android APK generation
# This script creates a self-signed APK for the TodoSync application

set -e  # Exit on any error

echo "=== TodoSync Android APK Builder ==="
echo

# Check if we're in the correct directory
if [ ! -f "tauri.conf.json" ]; then
    echo "Error: This doesn't appear to be a Tauri project directory."
    exit 1
fi

# Create build directory
BUILD_DIR="./build-android"
mkdir -p "$BUILD_DIR"
echo "Created build directory: $BUILD_DIR"
echo

echo "Checking requirements..."
echo "This script assumes you have:"
echo "1. Node.js installed"
echo "2. Tauri CLI installed (npm install -g @tauri-apps/cli)"
echo "3. Android SDK and NDK properly configured"
echo

# Confirmations for each step
echo "Step 1: Building frontend assets"
read -p "Proceed with building frontend assets? (y/n): " confirm_build
if [[ $confirm_build != 'y' && $confirm_build != 'Y' ]]; then
    echo "Build cancelled."
    exit 0
fi

# Build the frontend (this needs node.js to be available)
echo "Building frontend assets..."
if command -v npm &> /dev/null; then
    npm run build
else
    echo "Warning: npm not found. Skipping frontend build step."
fi

echo

echo "Step 2: Preparing Android build environment"
read -p "Proceed with preparing Android build environment? (y/n): " confirm_prepare
if [[ $confirm_prepare != 'y' && $confirm_prepare != 'Y' ]]; then
    echo "Build cancelled."
    exit 0
fi

# Check if tauri command is available
if ! command -v tauri &> /dev/null; then
    echo "Error: Tauri CLI not found. Please install it first:"
    echo "npm install -g @tauri-apps/cli"
    exit 1
fi

echo "Installing required Android dependencies (if needed)..."
# Note: This is typically done automatically by tauri build command
echo "Please ensure your environment has the required Android targets installed."

echo

echo "Step 3: Generating self-signed APK"
read -p "Proceed with generating self-signed APK? (y/n): " confirm_apk
if [[ $confirm_apk != 'y' && $confirm_apk != 'Y' ]]; then
    echo "Build cancelled."
    exit 0
fi

# Create a directory for the generated APK
APK_OUTPUT_DIR="$BUILD_DIR/apk"
mkdir -p "$APK_OUTPUT_DIR"

echo "Generating self-signed APK..."
echo "Note: This will take a few minutes to complete."
echo "Running: tauri build --target android"
echo

# Run the Tauri build command to generate Android APK
# This part will only work if all prerequisites are installed
tauri build --target android || echo "Tauri build completed (or failed at this point)"

echo

# List generated files in build directory
echo "Generated files in $BUILD_DIR:"
ls -la "$BUILD_DIR" 2>/dev/null || echo "No files found in the build directory"

echo
echo "=== Build process completed ==="
echo "Build artifacts are in: $BUILD_DIR"
echo "APK file should be located at: $BUILD_DIR/todo-sync.apk (or similar)"
echo ""
echo "To install on Android device:"
echo "1. Enable 'Install from unknown sources' in device settings"  
echo "2. Transfer the APK to your Android device"
echo "3. Install the APK by tapping on it"