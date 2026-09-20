from fastapi import APIRouter, HTTPException
from typing import List
from .. import models, db
from ..db import get_db_connection
import sqlite3

router = APIRouter(prefix="/conflict-logs", tags=["Conflict Logs"])

@router.get("/", response_model=List[models.ConflictLog])
def read_conflict_logs(skip: int = 0, limit: int = 100):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM conflict_logs ORDER BY timestamp DESC LIMIT ? OFFSET ?", (limit, skip))
        rows = cursor.fetchall()
        return [models.ConflictLog(**row) for row in rows]
    finally:
        connection.close()

@router.post("/", response_model=models.ConflictLog)
def create_conflict_log(conflict_log: models.ConflictLogCreate):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
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
        
        log_id = cursor.lastrowid
        cursor.execute("SELECT * FROM conflict_logs WHERE id = ?", (log_id,))
        row = cursor.fetchone()
        return models.ConflictLog(**row)
    finally:
        connection.close()

@router.get("/{log_id}", response_model=models.ConflictLog)
def read_conflict_log(log_id: int):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM conflict_logs WHERE id = ?", (log_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Conflict log not found")
        return models.ConflictLog(**row)
    finally:
        connection.close()