# TodoSync API Documentation

## Overview

This document provides comprehensive documentation for the TodoSync REST API and WebSocket endpoints. The API supports full CRUD operations for todo items with synchronization capabilities across multiple devices.

## Base URL

All API endpoints are accessible at:
```
http://192.168.2.2:8000/api/v1/
```

## Authentication

The API uses a simple approach without authentication in the development version but supports future authentication integration:

- **No Authentication Required**: All endpoints are publicly accessible
- **Security Note**: In production environments, implement appropriate security measures

## REST API Endpoints

### Todos Management

#### Get All Todos
```http
GET /api/v1/todos
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the TodoSync application",
    "completed": false,
    "created_at": "2026-09-20T10:00:00Z",
    "updated_at": "2026-09-20T10:00:00Z",
    "sequence_number": 1
  }
]
```

#### Create Todo
```http
POST /api/v1/todos
Content-Type: application/json

{
  "title": "New Task",
  "description": "Task description",
  "completed": false
}
```

**Response:**
```json
{
  "id": 2,
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-09-20T10:00:00Z",
  "updated_at": "2026-09-20T10:00:00Z",
  "sequence_number": 1
}
```

#### Get Todo by ID
```http
GET /api/v1/todos/{id}
```

**Response:**
```json
{
  "id": 2,
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-09-20T10:00:00Z",
  "updated_at": "2026-09-20T10:00:00Z",
  "sequence_number": 1
}
```

#### Update Todo
```http
PUT /api/v1/todos/{id}
Content-Type: application/json

{
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true,
  "sequence_number": 2
}
```

**Response:**
```json
{
  "id": 2,
  "title": "Updated Task",
  "description": "Updated description", 
  "completed": true,
  "created_at": "2026-09-20T10:00:00Z",
  "updated_at": "2026-09-20T10:01:00Z",
  "sequence_number": 2
}
```

#### Delete Todo
```http
DELETE /api/v1/todos/{id}
```

**Response:**
```json
{
  "message": "Todo deleted successfully"
}
```

### Conflict Logs

#### Get All Conflict Logs
```http
GET /api/v1/conflict-logs
```

**Response:**
```json
[
  {
    "id": 1,
    "todo_id": 2,
    "client_id": "device-123",
    "operation": "update",
    "original_data": "{\"title\":\"Task\",\"completed\":false}",
    "new_data": "{\"title\":\"Updated Task\",\"completed\":true}",
    "resolved": false,
    "timestamp": "2026-09-20T10:02:00Z"
  }
]
```

#### Get Conflict Log by ID
```http
GET /api/v1/conflict-logs/{id}
```

**Response:**
```json
{
  "id": 1,
  "todo_id": 2,
  "client_id": "device-123",
  "operation": "update",
  "original_data": "{\"title\":\"Task\",\"completed\":false}",
  "new_data": "{\"title\":\"Updated Task\",\"completed\":true}",
  "resolved": false,
  "timestamp": "2026-09-20T10:02:00Z"
}
```

## WebSocket Endpoints

### Connect to WebSocket
```http
ws://192.168.2.2:8000/ws/{todo_id}
```

**WebSocket Messages:**

#### Todo Created
```json
{
  "type": "todo_created",
  "data": {
    "id": 3,
    "title": "New Task",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-09-20T10:00:00Z",
    "updated_at": "2026-09-20T10:00:00Z",
    "sequence_number": 1
  }
}
```

#### Todo Updated 
```json
{
  "type": "todo_updated",
  "data": {
    "id": 2,
    "title": "Updated Task",
    "description": "Updated description",
    "completed": true,
    "created_at": "2026-09-20T10:00:00Z",
    "updated_at": "2026-09-20T10:01:00Z",
    "sequence_number": 2
  }
}
```

#### Todo Deleted
```json
{
  "type": "todo_deleted",
  "data": {
    "id": 2,
    "title": "Updated Task"
  }
}
```

### Client-Side Message Format

When sending messages to the WebSocket:

#### Update Operation with Sequence Number
```json
{
  "operation": "update",
  "id": 2,
  "data": {
    "title": "Updated Task",
    "description": "Updated description",
    "completed": true
  },
  "sequence_number": 3
}
```

## Error Responses

All API endpoints return appropriate HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Internal Server Error |

## Data Models

### Todo Model
```json
{
  "id": integer,
  "title": string,
  "description": string,
  "completed": boolean,
  "created_at": datetime,
  "updated_at": datetime,
  "sequence_number": integer
}
```

### Conflict Log Model
```json
{
  "id": integer,
  "todo_id": integer,
  "client_id": string,
  "operation": string,
  "original_data": string,
  "new_data": string,
  "resolved": boolean,
  "timestamp": datetime
}
```

## Sequence Number Handling

The system implements Last Write Wins (LWW) conflict resolution using sequence numbers:

1. Each todo operation increments the sequence number
2. When conflicts occur, client with higher sequence number wins
3. Sequence numbers must be incremented atomically during operations
4. All WebSocket operations include the current sequence number for conflict resolution

## Rate Limits

The API implements reasonable rate-limiting to prevent abuse:
- 100 requests per minute for unauthenticated endpoints
- 500 requests per minute for authenticated endpoints (planned)

## Security Considerations

1. **Input Validation**: All inputs are validated and sanitized
2. **Database Transactions**: All operations are run in database transactions
3. **No Sensitive Data Log**: No authentication tokens or sensitive data stored in logs
4. **LWW Conflict Resolution**: Safe resolution using sequence numbers rather than dangerous eval()

## Versioning

API versioning follows semantic versioning:
- `/api/v1/` - Current stable version
- Future versions: `/api/v2/`, `/api/v3/`, etc.

## Testing

The API has comprehensive unit tests covering all endpoints and edge cases including:
- Network disconnection scenarios
- Concurrent write operations  
- Sequence number management during sync
- Conflict resolution under various conditions