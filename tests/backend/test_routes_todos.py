import pytest
from unittest.mock import Mock, patch
from backend.routes.todos import (
    read_todos,
    read_todo,
    create_todo,
    update_todo,
    delete_todo,
    websocket_endpoint,
    handle_todo_websocket_update,
    handle_todo_create_websocket,
    handle_todo_update_websocket,
    handle_todo_delete_websocket
)
from fastapi import WebSocket
from backend.models import Todo, TodoCreate, TodoUpdate

# Test für read_todos
def test_read_todos():
    mock_db = Mock()
    mock_db.execute.return_value.fetchall.return_value = []
    
    result = read_todos(skip=0, limit=100, db=mock_db)
    assert isinstance(result, list)

# Test für read_todo
def test_read_todo():
    mock_db = Mock()
    mock_db.execute.return_value.fetchone.return_value = None
    
    result = read_todo(1, db=mock_db)
    assert result is None

# Test für create_todo
def test_create_todo():
    mock_db = Mock()
    mock_db.execute.return_value.fetchone.return_value = {"id": 1, "title": "Test", "sequence_number": 1}
    
    todo_data = TodoCreate(title="Test", completed=False)
    result = create_todo(todo_data, db=mock_db)
    assert result is not None

# Test für update_todo
def test_update_todo():
    mock_db = Mock()
    mock_db.execute.return_value.fetchone.return_value = {"id": 1, "title": "Updated Test", "sequence_number": 2}
    
    todo_update = TodoUpdate(title="Updated Test")
    result = update_todo(1, todo_update, db=mock_db)
    assert result is not None

# Test für delete_todo
def test_delete_todo():
    mock_db = Mock()
    mock_db.execute.return_value.fetchone.return_value = {"id": 1, "title": "Test", "sequence_number": 1}
    
    result = delete_todo(1, db=mock_db)
    assert result is not None

# Test für WebSocket-Funktionen
def test_handle_todo_websocket_update():
    # Mock-WebSocket und Daten
    websocket = Mock()
    websocket.send_text = Mock()
    message_data = {"action": "update", "data": {"id": 1, "title": "Updated", "sequence_number": 2}}
    
    result = handle_todo_websocket_update(message_data, 1, websocket)
    # Diese Funktion sollte nichts zurückgeben
    assert result is None

def test_handle_todo_create_websocket():
    websocket = Mock()
    websocket.send_text = Mock()
    data = {"action": "create", "data": {"id": 1, "title": "Test", "sequence_number": 1}}
    
    result = handle_todo_create_websocket(data, 1, websocket)
    assert result is None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])