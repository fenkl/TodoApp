import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from .models import ConflictLog, ConflictLogCreate, Todo
from .db import get_db_connection

def handle_todo_conflict(todo_id: int, client_id: str, operation: str, new_data: dict, existing_data: dict) -> bool:
    """
    Handle conflicts according to Last Write Wins (LWW) principle.
    
    Returns True if the conflict was logged, False otherwise.
    """
    connection = get_db_connection()
    
    try:
        cursor = connection.cursor()
        
        # Log the conflict for future analysis
        conflict_log = ConflictLogCreate(
            todo_id=todo_id,
            client_id=client_id,
            operation=operation,
            original_data=existing_data,
            new_data=new_data,
            resolved=False,
            timestamp=datetime.utcnow().isoformat()
        )
        
        cursor.execute('''
            INSERT INTO conflict_logs (todo_id, client_id, operation, original_data, new_data, resolved, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            conflict_log.todo_id,
            conflict_log.client_id,
            conflict_log.operation,
            str(conflict_log.original_data),
            str(conflict_log.new_data),
            conflict_log.resolved,
            conflict_log.timestamp
        ))
        
        connection.commit()
        return True
        
    except Exception as e:
        print(f"Error logging conflict: {e}")
        return False
    finally:
        connection.close()

def get_conflict_logs_for_todo(todo_id: int, limit: int = 50) -> List[ConflictLog]:
    """
    Retrieve conflict logs for a specific todo item.
    """
    connection = get_db_connection()
    
    try:
        cursor = connection.cursor()
        
        cursor.execute('''
            SELECT id, todo_id, client_id, operation, original_data, new_data, resolved, timestamp
            FROM conflict_logs 
            WHERE todo_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (todo_id, limit))
        
        rows = cursor.fetchall()
        return [
            ConflictLog(
                id=row[0],
                todo_id=row[1],
                client_id=row[2],
                operation=row[3],
                original_data=json.loads(row[4]) if row[4] else {},
                new_data=json.loads(row[5]) if row[5] else {},
                resolved=row[6],
                timestamp=row[7]
            ) for row in rows
        ]
        
    except Exception as e:
        print(f"Error retrieving conflict logs: {e}")
        return []
    finally:
        connection.close()

def apply_lww_resolution(todo_id: int, new_data: Dict[str, Any], client_sequence_number: int) -> bool:
    """
    Apply LWW resolution to determine the final state based on sequence numbers.
    
    This function should be called during an update operation to resolve conflicts
    using the Last Write Wins principle with sequence numbers.
    """
    connection = get_db_connection()
    
    try:
        cursor = connection.cursor()
        
        # Get current todo data and its sequence number
        cursor.execute('''
            SELECT id, title, description, completed, sequence_number, updated_at 
            FROM todos WHERE id = ?
        ''', (todo_id,))
        
        row = cursor.fetchone()
        if not row:
            return False
            
        current_todo = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'completed': bool(row[3]),
            'sequence_number': row[4],
            'updated_at': row[5]
        }
        
        # Compare sequence numbers to determine which update "wins"
        if client_sequence_number > current_todo['sequence_number']:
            # Client's version wins - update the todo with new data
            cursor.execute('''
                UPDATE todos 
                SET title = ?, description = ?, completed = ?, updated_at = CURRENT_TIMESTAMP, sequence_number = ?
                WHERE id = ?
            ''', (
                new_data.get('title', current_todo['title']),
                new_data.get('description', current_todo['description']),
                new_data.get('completed', current_todo['completed']),
                client_sequence_number,
                todo_id
            ))
            
            connection.commit()
            return True
        else:
            # Current version wins - do nothing, but we could return the resolved data to the client
            return False
            
    except Exception as e:
        print(f"Error applying LWW resolution: {e}")
        return False
    finally:
        connection.close()

def resolve_conflict(conflict_id: int, resolution: dict) -> bool:
    """
    Mark a conflict as resolved with the provided resolution.
    """
    connection = get_db_connection()
    
    try:
        cursor = connection.cursor()
        
        cursor.execute('''
            UPDATE conflict_logs 
            SET resolved = ?, resolution = ?
            WHERE id = ?
        ''', (True, json.dumps(resolution), conflict_id))
        
        connection.commit()
        return True
        
    except Exception as e:
        print(f"Error resolving conflict: {e}")
        return False
    finally:
        connection.close()

def get_latest_conflict_resolution(todo_id: int) -> Optional[Dict[str, Any]]:
    """
    Get the latest resolution for a todo item.
    """
    connection = get_db_connection()
    
    try:
        cursor = connection.cursor()
        
        cursor.execute('''
            SELECT resolution 
            FROM conflict_logs 
            WHERE todo_id = ? AND resolved = 1
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (todo_id,))
        
        row = cursor.fetchone()
        return json.loads(row[0]) if row and row[0] else None
        
    except Exception as e:
        print(f"Error getting conflict resolution: {e}")
        return None
    finally:
        connection.close()