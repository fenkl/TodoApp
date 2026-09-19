from . import models, db
from .db import get_db_connection_context
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_todo_conflict(todo_id: int, local_updated_at: datetime, remote_updated_at: datetime, action: str, conflict_type: str, details: str = None) -> bool:
    """
    Handle conflicts using Last Write Wins strategy.
    
    Args:
        todo_id: ID of the todo item that has a conflict
        local_updated_at: Timestamp from the local client
        remote_updated_at: Timestamp from the remote client
        action: The action that caused the conflict (create, update, delete)
        conflict_type: Type of conflict (e.g., "timestamp_conflict")
        details: Additional details about the conflict
        
    Returns:
        bool: True if conflict was resolved, False otherwise
    """
    
    # Determine which update is newer
    if local_updated_at > remote_updated_at:
        winner = "local"
        loser_updated_at = remote_updated_at
    else:
        winner = "remote"
        loser_updated_at = local_updated_at
        
    # Log the conflict
    conflict_log = models.ConflictLogCreate(
        todo_id=todo_id,
        action=action,
        conflict_type=conflict_type,
        details=f"Conflict resolved: {winner} wins. Local: {local_updated_at}, Remote: {remote_updated_at}"
    )
    
    try:
        with get_db_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conflict_logs (todo_id, action, conflict_type, details) VALUES (?, ?, ?, ?)",
                (conflict_log.todo_id, conflict_log.action, conflict_log.conflict_type, conflict_log.details)
            )
            conn.commit()
            logger.info(f"Conflict logged for todo {todo_id}: {winner} wins")
            
        return True
    except Exception as e:
        logger.error(f"Failed to log conflict for todo {todo_id}: {e}")
        return False

def get_conflict_logs_for_todo(todo_id: int, limit: int = 50):
    """
    Retrieve recent conflict logs for a specific todo.
    
    Args:
        todo_id: ID of the todo item
        limit: Maximum number of logs to return
        
    Returns:
        List of conflict logs
    """
    with get_db_connection_context() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM conflict_logs WHERE todo_id = ? ORDER BY created_at DESC LIMIT ?", 
            (todo_id, limit)
        )
        logs = cursor.fetchall()
        return [models.ConflictLog.from_attributes(log) for log in logs]