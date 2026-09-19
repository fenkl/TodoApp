from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, db
from ..db import get_db_connection
import sqlite3

router = APIRouter()

@router.get("/", response_model=List[models.ConflictLog])
async def read_conflict_logs(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM conflict_logs ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, skip))
    logs = cursor.fetchall()
    return [models.ConflictLog.from_attributes(log) for log in logs]

@router.post("/", response_model=models.ConflictLog)
async def create_conflict_log(conflict_log: models.ConflictLogCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO conflict_logs (todo_id, action, conflict_type, details) VALUES (?, ?, ?, ?) RETURNING id",
        (conflict_log.todo_id, conflict_log.action, conflict_log.conflict_type, conflict_log.details)
    )
    db.commit()
    log_id = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM conflict_logs WHERE id = ?", (log_id,))
    new_log = cursor.fetchone()
    return models.ConflictLog.from_attributes(new_log)

@router.get("/{log_id}", response_model=models.ConflictLog)
async def read_conflict_log(log_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM conflict_logs WHERE id = ?", (log_id,))
    log = cursor.fetchone()
    if log is None:
        raise HTTPException(status_code=404, detail="Conflict log not found")
    return models.ConflictLog.from_attributes(log)