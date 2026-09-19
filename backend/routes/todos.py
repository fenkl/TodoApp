from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from .. import models, db
from ..db import get_db_connection_context
import sqlite3
import json
from datetime import datetime

router = APIRouter()

# In-memory store for active WebSocket connections
active_connections = {}

@router.get("/", response_model=List[models.Todo])
async def read_todos(skip: int = 0, limit: int = 100):
    with get_db_connection_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos ORDER BY updated_at DESC LIMIT ? OFFSET ?", (limit, skip))
        todos = cursor.fetchall()
        return [models.Todo.from_attributes(todo) for todo in todos]

@router.get("/{todo_id}", response_model=models.Todo)
async def read_todo(todo_id: int):
    with get_db_connection_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        todo = cursor.fetchone()
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return models.Todo.from_attributes(todo)

@router.post("/", response_model=models.Todo)
async def create_todo(todo: models.TodoCreate):
    with get_db_connection_context() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?) RETURNING id",
            (todo.title, todo.description, todo.completed)
        )
        conn.commit()
        todo_id = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        new_todo = cursor.fetchone()
        return models.Todo.from_attributes(new_todo)

@router.put("/{todo_id}", response_model=models.Todo)
async def update_todo(todo_id: int, todo_update: models.TodoUpdate):
    with get_db_connection_context() as conn:
        cursor = conn.cursor()
        
        # Get the existing todo to check for conflicts
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        existing_todo = cursor.fetchone()
        
        if existing_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # Prepare update fields
        update_fields = []
        params = []
        
        if todo_update.title is not None:
            update_fields.append("title = ?")
            params.append(todo_update.title)
        if todo_update.description is not None:
            update_fields.append("description = ?")
            params.append(todo_update.description)
        if todo_update.completed is not None:
            update_fields.append("completed = ?")
            params.append(todo_update.completed)
        
        # Add updated_at timestamp
        update_fields.append("updated_at = datetime('now')")
        
        # Add ID to parameters
        params.append(todo_id)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        # Execute update
        query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        
        # Get the updated todo
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        updated_todo = cursor.fetchone()
        
        if updated_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        return models.Todo.from_attributes(updated_todo)

@router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    with get_db_connection_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        todo = cursor.fetchone()
        
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        return {"message": "Todo deleted successfully"}

# WebSocket endpoint for synchronization
@router.websocket("/ws/sync")
async def websocket_endpoint(websocket: WebSocket, todo_id: int = None):
    await websocket.accept()
    
    # Store the connection
    if todo_id not in active_connections:
        active_connections[todo_id] = []
    active_connections[todo_id].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
            
    except WebSocketDisconnect:
        # Remove the connection when disconnected
        if todo_id in active_connections:
            active_connections[todo_id].remove(websocket)
            if not active_connections[todo_id]:
                del active_connections[todo_id]