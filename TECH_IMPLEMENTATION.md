# Technical Implementation Documentation

## Overview

This document provides comprehensive technical documentation for the TodoSync cross-platform todo application. The system implements real-time synchronization with conflict resolution using a Last Write Wins (LWW) strategy, offline support, and LAN-based communication.

## Architecture

### System Components

1. **Frontend (Svelte-based)**
   - Svelte components for UI rendering
   - WebSocket integration for real-time updates
   - Offline queue system for handling network interruptions
   - API wrapper for backend communication  

2. **Backend (FastAPI)**
   - REST API endpoints for todo management
   - WebSocket endpoints for real-time synchronization
   - SQLite database with conflict tracking
   - Conflict resolution mechanism

3. **Tauri Integration**
   - Cross-platform window management
   - Android build support 
   - Native system integration

## Project Structure

```
.
├── backend/                 # FastAPI backend application
│   ├── routes/              # API route handlers
│   │   ├── conflict_logs.py # Conflict logging endpoints
│   │   └── todos.py         # Todo management endpoints  
│   ├── conflict_handler.py  # Conflict resolution logic
│   ├── db.py                # Database initialization and connection handling
│   ├── main.py              # FastAPI application entry point
│   └── models.py            # Data models for API contracts
├── frontend/                # Frontend assets and configurations
│   ├── src/                 # Svelte source code  
│   │   ├── App.svelte       # Main application component
│   │   ├── components/      # UI components
│   │   │   ├── TodoList.svelte     # Todo list management
│   │   │   └── ConflictLogPanel.svelte  # Conflict log display
│   │   └── lib/             # Utility libraries
│   │       ├── api.ts       # REST API client
│   │       ├── offline-queue.ts  # Offline action queueing
│   │       └── ws.ts        # WebSocket connection manager
│   ├── src-tauri/           # Tauri application code  
│   │   ├── src/main.rs      # Entry point for Tauri app
│   │   └── src/todo_sync.rs # Tauri integration logic
│   └── package.json         # Frontend dependencies and scripts
└── tauri.conf.json          # Tauri configuration
```

## Database Schema

The backend database uses SQLite with the following schema:

### Todos Table
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sequence_number INTEGER DEFAULT 0
);
```

### Conflict Logs Table  
```sql
CREATE TABLE conflict_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    todo_id INTEGER NOT NULL,
    client_id TEXT NOT NULL,
    operation TEXT NOT NULL,  -- 'create', 'update', 'delete'
    original_data TEXT,
    new_data TEXT,
    resolved BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Backend Implementation

### API Endpoints

#### Todos Endpoint
- `GET /api/v1/todos` - Retrieve all todos
- `POST /api/v1/todos` - Create a new todo  
- `PUT /api/v1/todos/{id}` - Update an existing todo
- `DELETE /api/v1/todos/{id}` - Delete a todo

#### Conflict Logs Endpoint
- `GET /api/v1/conflict-logs` - Retrieve all conflict logs
- `POST /api/v1/conflict-logs` - Create new conflict log
- `GET /api/v1/conflict-logs/{id}` - Retrieve specific conflict log

### WebSocket Endpoints

The backend implements WebSocket support for real-time updates:
- `/ws/{todo_id}` - WebSocket connection endpoint for specific todos
- Messages are broadcast to all connected clients
- Support for todo creation, update, and delete operations with sequence numbers

### Conflict Resolution

#### Last Write Wins (LWW) Principle
The system implements a robust LWW conflict resolution mechanism:

1. **Sequence Number Tracking**: Each todo maintains a `sequence_number` field to track versioning
2. **Conflict Detection**: When conflicts occur during updates, the system logs them
3. **Resolution Logic**: The client with the higher sequence number "wins" 
4. **Database Updates**: Only the winning version is applied to the database

#### Conflict Handler Functions
- `handle_todo_conflict()` - Logs conflicts to the database
- `apply_lww_resolution()` - Implements LWW resolution using sequence numbers  
- `resolve_conflict()` - Marks specific conflicts as resolved
- `get_conflict_logs_for_todo()` - Retrieves conflict history for a todo

## Frontend Implementation

### Core Components

#### TodoList.svelte
- Displays and manages todo items  
- Handles user interactions for creating, updating, and deleting todos
- Integrates with the offline queue system

#### ConflictLogPanel.svelte
- Shows last 50 conflict logs for debugging
- Displays information about conflicts that occurred during synchronization

### Offline Queue System (offline-queue.ts)

The frontend implements a robust offline queue system:

1. **Persistent Storage**: Uses localStorage to persist queued actions
2. **Retry Logic**: Implements exponential backoff retry mechanism (max 3 retries)
3. **Sequence Number Tracking**: Assigns sequence numbers to queued actions for conflict resolution  
4. **Automatic Sync**: Periodically attempts to sync queued actions when connection is restored

### WebSocket Integration (ws.ts)

The frontend connects to the backend via WebSocket with:
1. **Reconnection Logic**: Automatic reconnection with exponential backoff
2. **Sequence Number Management**: Maintains sequence numbers for operations
3. **Operation Broadcasting**: Sends todo operations with sequence numbers to the backend

### API Client (api.ts)

Provides REST API wrapper functions:
- `fetchTodos()` - Retrieve all todos from backend
- `createTodo()`, `updateTodo()`, `deleteTodo()` - CRUD operations
- `fetchConflictLogs()` - Retrieve conflict logs for debugging

## Synchronization Flow

### Normal Operation
1. User performs todo operation (create/update/delete)
2. Action is sent to the backend via REST API or WebSocket
3. Backend validates and processes the operation  
4. WebSocket broadcast notifies connected clients
5. All clients update their UI immediately

### Offline Operations
1. When network disconnected, operations are queued locally  
2. Queue uses localStorage persistence
3. On reconnect, queue is processed serially with retry mechanism
4. Sequence numbers are used for LWW conflict resolution during sync

### Conflict Resolution Process
1. Client detects a concurrent write during update 
2. Backend logs the conflict to `conflict_logs` table
3. When client tries to sync, it sends sequence number along with operation
4. Backend compares sequence numbers:
   - Higher sequence number "wins" 
   - The winning version is applied to database
   - Conflicts are marked as resolved

## Security Improvements

### Conflict Log Parsing
- Replaced dangerous `eval()` with safe `json.loads()`/`json.dumps()`
- All conflict log data is now parsed using secure JSON methods

### Data Validation
- Backend validates all incoming requests using Pydantic models
- Proper error handling for HTTP status codes
- Input sanitization and validation throughout the system

## Cross-Platform Support

### Tauri Integration
1. **Multi-platform Deployment**: Build targets include Linux, Windows, macOS, and Android
2. **Android Support**: Includes proper configuration for Android builds  
3. **Window Management**: Desktop versions use 800x600 window size
4. **Bundle Configuration**: Uses `com.todosync.app` as bundle identifier

### Device Detection
- Automatically detects device type and sets appropriate parameters
- Supports different handling based on platform (Linux, Windows, Android, etc.)

## Build & Development

### Prerequisites
- Node.js and npm for frontend development  
- Rust toolchain for Tauri builds
- Android development tools for mobile builds

### Commands
- `npm run dev` - Start development server
- `npm run tauri android dev` - Build and run Android app
- `npm run tauri android build --release` - Generate release .aab file  

## Testing

1. Start backend server at `http://192.168.2.2:8000`
2. Connect Android device/emulator to same LAN network  
3. Run `npm run tauri android dev` for testing
4. Use `npm run tauri android build --release` for release package generation

## Edge Case Handling

### Network Interruptions
- Automatic offline queueing of operations
- Reconnection logic with exponential backoff
- Queue persistence between app sessions

### Concurrent Writes
- LWW conflict resolution using sequence numbers  
- Proper database transactions for atomic operations
- Conflict logging and tracking system

### WebSocket Errors
- Comprehensive error handling and reconnection
- Message queuing during disconnection periods  
- Proper cleanup of WebSocket connections

## Performance Considerations

1. **Database Transactions**: Uses SQLite transactions to ensure data integrity
2. **Sequence Number Management**: Optimized for performance in conflict resolution
3. **Offline Queue Processing**: Serialized processing to prevent race conditions
4. **Memory Management**: Efficient use of localStorage and browser resources