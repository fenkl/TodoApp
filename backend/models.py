from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ConflictLogCreate(BaseModel):
    todo_id: int
    client_id: str
    operation: str  # 'create', 'update', 'delete'
    original_data: dict  # The data before the conflict
    new_data: dict     # The data that caused the conflict
    resolved: bool = False
    timestamp: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ConflictLog(ConflictLogCreate):
    id: int
    
    class Config:
        from_attributes = True

class SyncMessage(BaseModel):
    type: str  # 'update', 'create', 'delete'
    data: dict
    timestamp: str
    client_id: str

class TodoConflictInfo(BaseModel):
    todo_id: int
    conflict_type: str  # e.g., 'lww', 'timestamp_conflict'
    details: dict
    resolved: bool = False