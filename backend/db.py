import sqlite3
from typing import Optional
import os
from contextlib import contextmanager

# Database file path
DB_PATH = "todo_sync.db"

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    
    # Enable WAL mode
    conn.execute("PRAGMA journal_mode=WAL")
    
    cursor = conn.cursor()
    
    # Create todos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create conflict_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conflict_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            todo_id INTEGER,
            action TEXT,
            conflict_type TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (todo_id) REFERENCES todos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

@contextmanager
def get_db_connection_context():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    try:
        yield conn
    finally:
        conn.close()