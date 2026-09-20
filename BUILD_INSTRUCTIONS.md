# TodoSync Build and Package Generation Guide

## Overview
This document provides comprehensive instructions for building and packaging the TodoSync application across different platforms and target devices.

## Prerequisites

### Required Software
- **Node.js** (v16 or later) 
- **Rust** and **Cargo** (for Tauri)
- **Python 3** with pip
- **Git**

### Platform-Specific Requirements

#### Linux
- `build-essential` package
- `libwebkit2gtk-4.0-dev`
- `libappindicator3-dev`
- `libsecret-1-dev`

#### macOS
- Xcode command line tools (`xcode-select --install`)
- Homebrew (for package management)

#### Windows
- Visual Studio with C++ build tools
- Windows SDK

## Building the Application

### 1. Initial Setup

Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd TodoApp
npm install
```

### 2. Backend Setup
```bash
# Install Python requirements
pip install -r requirements.txt
```

### 3. Build Commands

#### Desktop Applications

For Linux:
```bash
# Build AppImage package
tauri build --target appimage

# Build RPM package  
tauri build --target rpm
```

For Windows:
```bash
tauri build --target windows
```

For macOS:
```bash
tauri build --target macos
```

#### Android Application
```bash
# Follow Android-specific build process in ANDROID_BUILD_GUIDE.md
./build.sh
```

## Cross-Platform Build Target Summary

| Platform | Build Command | Output Format |
|----------|---------------|---------------|
| Linux AppImage | `tauri build --target appimage` | .AppImage |
| Linux RPM | `tauri build --target rpm` | .rpm |
| macOS | `tauri build --target macos` | .dmg |
| Windows | `tauri build --target windows` | .exe |
| Android | `tauri build --target android` | .apk |

## Development Environment

### Development Server
```bash
# Start development server
npm run dev
```

### Testing
```bash
# Run backend tests
cd backend
python -m pytest tests/

# Run frontend tests
npm test
```

## Troubleshooting

### Common Issues
1. **Missing rustup**: Install Rust with `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. **Webpack errors**: Clear cache and reinstall modules: `rm -rf node_modules && npm install`
3. **Tauri build failures**: Ensure all prerequisites are installed

### Environment Variables
Set environment variables as needed in your `.env` file:
```bash
# Example .env file contents
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

## Packaging for Distribution

The application is built using Tauri's cross-platform capabilities, generating packages for different target platforms with appropriate icons and metadata.

### Package Structure
After building, the following files will be generated:
- `src-tauri/target/<target>/release/bundle/`
- Package files with appropriate extensions for each operating system.

## Security Considerations

### Codebase Updates
Regularly update dependencies to maintain security posture:

```bash
# Update Node.js packages
npm update

# Update Python packages  
pip list --outdated
pip install --upgrade <package-name>
```

### Vulnerability Scanning
1. Run npm audit: `npm audit`
2. Run Python security checks with pip-audit or similar tools

## Support and Maintenance

For more information about the TodoSync application architecture, refer to:
- TECH_IMPLEMENTATION.md
- ROADMAP.md