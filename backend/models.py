from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ConflictLog(BaseModel):
    id: int
    todo_id: int
    action: str
    conflict_type: str
    details: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConflictLogCreate(BaseModel):
    todo_id: int
    action: str
    conflict_type: str
    details: Optional[str] = None

# WebSocket message models
class SyncMessage(BaseModel):
    type: str  # "updated", "created", "rejected"
    todo_id: int
    data: Optional[Todo] = None

class TodoConflictInfo(BaseModel):
    todo_id: int
    local_updated_at: datetime
    remote_updated_at: datetime