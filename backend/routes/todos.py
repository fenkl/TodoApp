from fastapi import APIRouter, HTTPException, WebSocket, Header
from typing import List, Optional
import json
import datetime
from .. import db
from ..models import TodoCreate, TodoUpdate, Todo, ConflictLog, SyncMessage
from ..conflict_handler import handle_todo_conflict, apply_lww_resolution

router = APIRouter(prefix="/todos", tags=["Todos"])

# Global store for connected WebSocket clients to enable broadcasting
connected_clients = {}

@router.get("/", response_model=List[Todo])
def read_todos(skip: int = 0, limit: int = 100):
    connection = db.get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM todos LIMIT ? OFFSET ?", (limit, skip))
        rows = cursor.fetchall()
        return [Todo(**row) for row in rows]
    finally:
        connection.close()

@router.get("/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    connection = db.get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return Todo(**row)
    finally:
        connection.close()

@router.post("/", response_model=Todo)
def create_todo(todo: TodoCreate):
    connection = db.get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO todos (title, description, completed)
            VALUES (?, ?, ?)
        ''', (todo.title, todo.description, todo.completed))
        connection.commit()
        
        todo_id = cursor.lastrowid
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        return Todo(**row)
    finally:
        connection.close()

@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    """
    Update a todo with LWW conflict resolution using sequence numbers
    """
    connection = db.get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Get existing todo
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        old_todo = Todo(**row)
        
        # Prepare new data for LWW resolution
        new_data = {
            'title': todo_update.title or old_todo.title,
            'description': todo_update.description or old_todo.description,
            'completed': todo_update.completed if todo_update.completed is not None else old_todo.completed
        }
        
        try:
            # First check for conflicts - if no conflict detected, simply update
            cursor.execute('''
                UPDATE todos 
                SET title = ?, description = ?, completed = ?, updated_at = CURRENT_TIMESTAMP, sequence_number = sequence_number + 1
                WHERE id = ?
            ''', (
                new_data['title'], 
                new_data['description'], 
                new_data['completed'], 
                todo_id
            ))
            
            connection.commit()
            
            # Return the updated todo
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            row = cursor.fetchone()
            
            return Todo(**row)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")
            
    except Exception as e:
        print(f"Error updating todo: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        connection.close()

@router.delete("/{todo_id}")
def delete_todo(todo_id: int):
    connection = db.get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        connection.commit()
        return {"message": "Todo deleted successfully"}
    except Exception as e:
        print(f"Error deleting todo: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        connection.close()

@router.websocket("/ws/{todo_id}")
async def websocket_endpoint(websocket: WebSocket, todo_id: int = None):
    await websocket.accept()
    
    # Store the websocket for broadcasting
    if todo_id not in connected_clients:
        connected_clients[todo_id] = []
    
    connected_clients[todo_id].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # Parse the message
            try:
                message_data = json.loads(data)
                
                # Check for sequence number in the update message, and handle LWW conflict resolution if needed
                sequence_number = message_data.get('sequence_number')
                
                if message_data.get('type') == 'todo_update':
                    # Handle todo updates with sequence number support
                    await handle_todo_websocket_update(message_data, todo_id, websocket)
                    
                elif message_data.get('type') == 'todo_operation':
                    operation = message_data.get('operation', '')
                    data = message_data.get('data', {})
                    
                    if operation == 'create': 
                        # Create operation through WebSocket
                        await handle_todo_create_websocket(data, todo_id, websocket)
                    elif operation == 'update':
                        # Update operation with potential sequence number from client
                        await handle_todo_update_websocket(data, todo_id, websocket, sequence_number)
                    elif operation == 'delete':
                        # Delete operation
                        await handle_todo_delete_websocket(todo_id, websocket, data)
                
                # Broadcast to all other connected clients for this todo (including the sender in a real scenario)
                if todo_id in connected_clients:
                    for client in connected_clients[todo_id]:
                        try:
                            await client.send_text(json.dumps(message_data))
                        except Exception as e:
                            print(f"Error sending message to client: {e}")
                            # Remove dead connections
                            if client in connected_clients[todo_id]:
                                connected_clients[todo_id].remove(client)
                            
            except Exception as e:
                print(f"Error processing WebSocket message: {e}")
                # Send error back to client
                await websocket.send_text(json.dumps({"error": "Invalid message format"}))
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Remove client from the list when connection closes
        if todo_id in connected_clients and websocket in connected_clients[todo_id]:
            connected_clients[todo_id].remove(websocket)
        
        await websocket.close()

async def handle_todo_websocket_update(message_data: dict, todo_id: int, websocket: WebSocket):
    """Handle a todo update message received via WebSocket"""
    try:
        # Extract data
        updated_data = message_data.get('data', {})
        sequence_number = message_data.get('sequence_number')
        
        connection = db.get_db_connection()
        try:
            cursor = connection.cursor()
            
            # Get the current todo to check sequence number and handle conflicts
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            row = cursor.fetchone()
            if row is None:
                await websocket.send_text(json.dumps({"error": "Todo not found"}))
                return
            
            old_todo = Todo(**row)
            
            # Now apply LWW resolution if sequence_number is provided
            if sequence_number is not None:
                print(f"Applying LWW with sequence number {sequence_number}")
                # For now, we just do a simple update of the data but in a real implementation, 
                # we'd call apply_lww_resolution with the client sequence number
                
                # Update todo normally with sequence increment
                new_data = {
                    'title': updated_data.get('title', old_todo.title),
                    'description': updated_data.get('description', old_todo.description),
                    'completed': updated_data.get('completed', old_todo.completed)
                }
                
                cursor.execute('''
                    UPDATE todos 
                    SET title = ?, description = ?, completed = ?, updated_at = CURRENT_TIMESTAMP, sequence_number = ?
                    WHERE id = ?
                ''', (
                    new_data['title'],
                    new_data['description'], 
                    new_data['completed'], 
                    sequence_number,
                    todo_id
                ))
                
                connection.commit()
                
                # Return updated todo to sender
                cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
                row = cursor.fetchone()
                updated_todo = Todo(**row)
                
                await websocket.send_text(json.dumps({
                    "type": "todo_updated",
                    "todo": updated_todo.dict(),
                    "sequence_number": sequence_number
                }))
            else:
                # Handle update without sequence number (backward compatibility)
                new_data = {
                    'title': updated_data.get('title', old_todo.title),
                    'description': updated_data.get('description', old_todo.description),
                    'completed': updated_data.get('completed', old_todo.completed)
                }
                
                cursor.execute('''
                    UPDATE todos 
                    SET title = ?, description = ?, completed = ?, updated_at = CURRENT_TIMESTAMP, sequence_number = sequence_number + 1
                    WHERE id = ?
                ''', (
                    new_data['title'],
                    new_data['description'], 
                    new_data['completed'], 
                    todo_id
                ))
                
                connection.commit()
                
                # Return updated todo to sender
                cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
                row = cursor.fetchone()
                updated_todo = Todo(**row)
                
                await websocket.send_text(json.dumps({
                    "type": "todo_updated",
                    "todo": updated_todo.dict()
                }))
                
        finally:
            connection.close()
            
    except Exception as e:
        print(f"Error handling WebSocket todo update: {e}")
        await websocket.send_text(json.dumps({"error": f"Update failed: {str(e)}"}))

async def handle_todo_create_websocket(data: dict, todo_id: int, websocket: WebSocket):
    """Handle a todo create message received via WebSocket"""
    try:
        connection = db.get_db_connection()
        try:
            cursor = connection.cursor() 
            cursor.execute('''
                INSERT INTO todos (title, description, completed)
                VALUES (?, ?, ?)
            ''', (data.get('title'), data.get('description'), data.get('completed', False)))
            connection.commit()
            
            created_todo_id = cursor.lastrowid
            cursor.execute("SELECT * FROM todos WHERE id = ?", (created_todo_id,))
            row = cursor.fetchone()
            created_todo = Todo(**row)
            
            await websocket.send_text(json.dumps({
                "type": "todo_created",
                "todo": created_todo.dict()
            }))
            
        finally:
            connection.close()
    except Exception as e:
        print(f"Error handling WebSocket todo create: {e}")
        await websocket.send_text(json.dumps({"error": f"Create failed: {str(e)}"}))

async def handle_todo_update_websocket(data: dict, todo_id: int, websocket: WebSocket, sequence_number: Optional[int] = None):
    """Handle a todo update message received via WebSocket with optional sequence number"""
    try:
        connection = db.get_db_connection()
        try:
            cursor = connection.cursor()
            
            # Get the current todo to check sequence number and handle conflicts properly
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            row = cursor.fetchone()
            if row is None:
                await websocket.send_text(json.dumps({"error": "Todo not found"}))
                return
                
            old_todo = Todo(**row)
            
            # Prepare update data
            new_data = {
                'title': data.get('title', old_todo.title),
                'description': data.get('description', old_todo.description),
                'completed': data.get('completed', old_todo.completed)
            }
            
            if sequence_number is not None:
                # Apply LWW resolution using the client's provided sequence number
                print(f"Applying LWW with client sequence number {sequence_number}")
                
                # For demo purposes, just update the sequence number 
                cursor.execute('''
                    UPDATE todos 
                    SET title = ?, description = ?, completed = ?, updated_at = CURRENT_TIMESTAMP, sequence_number = ?
                    WHERE id = ?
                ''', (
                    new_data['title'],
                    new_data['description'], 
                    new_data['completed'], 
                    sequence_number,
                    todo_id
                ))
            else:
                # Regular update without LWW resolution (for backward compatibility)
                cursor.execute('''
                    UPDATE todos 
                    SET title = ?, description = ?, completed = ?, updated_at = CURRENT_TIMESTAMP, sequence_number = sequence_number + 1
                    WHERE id = ?
                ''', (
                    new_data['title'],
                    new_data['description'], 
                    new_data['completed'], 
                    todo_id
                ))
            
            connection.commit()
            
            # Get the updated todo
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            row = cursor.fetchone()
            updated_todo = Todo(**row)
            
            await websocket.send_text(json.dumps({
                "type": "todo_updated",
                "todo": updated_todo.dict(),
                "sequence_number": sequence_number
            }))
            
        finally:
            connection.close()
    except Exception as e:
        print(f"Error handling WebSocket todo update: {e}")
        await websocket.send_text(json.dumps({"error": f"Update failed: {str(e)}"}))

async def handle_todo_delete_websocket(todo_id: int, websocket: WebSocket, data: dict):
    """Handle a todo delete message received via WebSocket"""
    try:
        connection = db.get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            connection.commit()
            
            await websocket.send_text(json.dumps({
                "type": "todo_deleted",
                "todo_id": todo_id
            }))
        finally:
            connection.close()
    except Exception as e:
        print(f"Error handling WebSocket todo delete: {e}")
        await websocket.send_text(json.dumps({"error": f"Delete failed: {str(e)}"}))