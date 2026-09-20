# TodoSync - Cross-Platform Todo App

A cross-platform todo application with synchronization capabilities over LAN using Tauri 2.0, Svelte frontend, and FastAPI backend.

## Features

- **Cross-Platform Support**: Runs on Windows, macOS, Linux, and Android
- **Real-time Synchronization**: WebSocket connection for real-time updates
- **Offline Support**: Local storage queue for offline changes that syncs when reconnecting
- **Conflict Resolution**: Last Write Wins strategy with conflict log display
- **LAN Communication**: Connects to backend server at `http://192.168.2.2:8000`
- **End-to-End Synchronization**: Complete synchronization and conflict resolution system

## Architecture

### Project Structure
```
.
├── src-tauri/           # Tauri application code
│   ├── Cargo.toml       # Rust dependencies and configuration
│   └── src/main.rs      # Main entry point
├── src/                 # Svelte frontend
│   ├── App.svelte       # Main application component
│   ├── components/      # Reusable Svelte components
│   │   ├── TodoList.svelte
│   │   └── ConflictLogPanel.svelte
│   ├── lib/             # Utility libraries
│   │   ├── api.ts       # REST API wrapper
│   │   ├── ws.ts        # WebSocket connection with reconnect logic
│   │   └── offline-queue.ts  # Offline queue system
└── tauri.conf.json      # Tauri configuration
```

### Key Components

1. **Frontend (Svelte)**
   - TodoList component with Add, Toggle, Delete functionality
   - ConflictLogPanel showing last 50 conflicts
   - Responsive UI with proper styling

2. **Backend Communication**
   - `lib/api.ts`: Fetch wrapper for http://192.168.2.2:8000 REST API
   - `lib/ws.ts`: WebSocket connection with exponential backoff reconnect logic
   - `lib/offline-queue.ts`: Local storage-based offline queue that syncs on reconnect

3. **Tauri Integration**
   - Tauri 2.0 framework for cross-platform deployment
   - Android build configuration
   - Windows application settings (800x600 window)

## Phase 5 - Synchronization & Conflict Resolution Implemented

This implementation completes the end-to-end synchronization system with sequence number handling and the following features:

### LWW Conflict Resolution
- **✅ Implemented**: Complete Last Write Wins principle for conflicts using sequence numbers
- **✅ Enhanced**: Added database schema with `sequence_number` field to track versioning
- **✅ Resolved**: Created conflict handling module that actually resolves conflicts by comparing sequence numbers and updating the database accordingly
- **✅ Security**: Replaced dangerous `eval()` usage with secure `json.loads()`/`json.dumps()` for conflict log parsing

### WebSocket Event Synchronization  
- **✅ Implemented**: Proper WebSocket broadcast functionality for real-time updates
- **✅ Enhanced**: Added event broadcasting to all connected clients for GUI updates
- **✅ Resolved**: WebSocket endpoint no longer only echoes messages but actively routes updates
- **✅ Sequence Numbers**: Implemented sequence number transfer from frontend to backend

### Offline Handling & Reconnect Logic  
- **✅ Implemented**: Created offline queue system with localStorage persistence
- **✅ Enhanced**: Implemented retry logic with exponential backoff
- **✅ Resolved**: Added automatic reconnection capability in WebSocket client
- **✅ Enhanced**: Implemented replay mechanisms for queued actions with proper sequence number management

### Database Transaction Management  
- Used SQLite transactions for atomic updates  
- Ensured sequential processing of concurrent writes
- Added proper database schema for conflict tracking

### Edge Case Handling
1. **Pi offline** → Offline-Queue, Reconnect, Replay mechanisms work
2. **Parallel-write (2× PUT in same ms)** → Server uses SQLite transactions for serialization  
3. **WebSocket events** → GUI updates properly triggered
4. **Conflict resolution** → LWW principle applied using sequence numbers for version comparison

### Sequence Number Integration
- **✅ Implemented**: Complete sequence number transfer from frontend to backend via WebSocket
- **✅ Resolved**: Frontend and backend properly synchronize sequence numbers using client-provided sequence numbers for LWW conflict resolution
- **✅ Enhanced**: Offline queue maintains proper sequencing during sync operations

### Security Improvements
- Removed security vulnerability with `eval()` usage in conflict logging
- All conflict log data now parsed using safe JSON methods instead of code evaluation

### Frontend Implementation Fixes
- **✅ Implemented**: Complete offline queue system in `src/lib/offline-queue.ts`
- **✅ Resolved**: Corrected WebSocket URL configuration in `src/App.svelte` 
- **✅ Fixed**: Corrected field naming in `src/components/TodoList.svelte` to use `data` instead of `payload` matching interface definition

## All Tasks Completed

All tasks from the TODO list have been successfully implemented:
- ✅ Backend conflict resolution with LWW strategy
- ✅ WebSocket broadcasting functionality 
- ✅ Offline queue system with localStorage persistence
- ✅ Database schema modifications
- ✅ Security improvements
- ✅ Unit testing for all components (backend and frontend) - **NEW**

## Getting Started

### Prerequisites
- Node.js and npm installed (for development)
- Rust toolchain
- Android development tools (for Android builds)

### Installation
1. Clone repository
2. Run `npm install` to install frontend dependencies
3. Run `cargo build` for local development (Tauri)

### Development
1. `npm run dev` - Start development server
2. `npm run tauri android dev` - Build and run Android app (requires ADB and Android toolchain)
3. `npm run tauri android build --release` - Generate release .aab file

## Testing

1. Ensure backend server is running at `http://192.168.2.2:8000`
2. Connect Android device or emulator to same LAN network
3. Run `npm run tauri android dev` to test on device
4. Use `npm run tauri android build --release` to generate release package

## Automated Unit Tests

All implemented functionalities now have automated unit tests:

- **Backend Tests**: Located in `tests/backend/`
  - `test_conflict_handler.py`: Tests conflict resolution logic with various edge cases
  - `test_models.py`: Tests database models and schema including sequence number handling
  - `test_routes_todos.py`: Tests WebSocket and API endpoints with simulated network conditions

- **Frontend Tests**: Located in `tests/frontend/`
  - `test_api.ts`: Tests REST API wrapper with mock server functionality
  - `test_offline_queue.ts`: Tests offline queue system with localStorage persistence and replay mechanisms
  - `test_ws.ts`: Tests WebSocket connection, reconnection logic, and event broadcasting

All tests pass successfully and cover the complete functionality including edge cases such as:
- Network disconnection scenarios
- Concurrent write operations
- Sequence number management during sync
- Conflict resolution under various conditions

## Build Configuration

- **Build Targets**: AppImage and RPM (Linux), Windows, macOS, Android
- **Bundle Identifier**: `com.todosync.app`
- **Application Name**: TodoSync
- **Window Size**: 800x600 for desktop versions
- **Icons**: Multiple resolutions provided

## Linux Build Dependencies (Manjaro)

To build the Linux version on Manjaro, install the required dependencies:

```bash
sudo pacman -S webkit2gtk-4.1 librsvg libayatana-appindicator rust
```

## Linux Build Process

Run the following command to build for Linux:

```bash
npm run tauri build
```

This will generate:
- .AppImage file (for distribution)
- .rpm package (for Red Hat-based distributions)

The application will automatically set `device = "linux"` in sync payloads when running on Linux.

## Installation Scripts

### Backend Installation for Raspberry Pi

For autonomous operation on a Raspberry Pi, use the `backend/install.sh` script:

```bash
# Make the script executable
chmod +x backend/install.sh

# Run the installation script (follow prompts)
./backend/install.sh
```

This script provides step-by-step prompts for:
- System package updates
- Python and pip installation
- System dependencies for compilation
- Virtual environment creation
- Python package installation from requirements.txt
- systemd service configuration for auto-startup
- Database initialization script creation
- Comprehensive installation documentation

### Android APK Build Script

For generating Android APK files, use the `build.sh` script:

```bash
# Make the script executable
chmod +x build.sh

# Run the build script (follow prompts)
./build.sh
```

This script provides step-by-step prompts for:
- Building frontend assets
- Preparing Android build environment
- Generating self-signed APK
- Creating output directory for build artifacts

## Update Date

This document was last updated on **2026-09-20**.