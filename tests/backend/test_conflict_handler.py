import pytest
import json
from unittest.mock import Mock, patch
from backend.conflict_handler import (
    handle_todo_conflict,
    apply_lww_resolution,
    resolve_conflict,
    get_conflict_logs_for_todo,
    get_latest_conflict_resolution
)
from backend.models import Todo

# Test für handle_todo_conflict Funktion
def test_handle_todo_conflict():
    # Mock der Datenbank
    mock_db = Mock()
    
    # Testdaten
    todo_id = 1
    existing_todo = {"id": 1, "title": "Test", "sequence_number": 1}
    incoming_todo = {"id": 1, "title": "Updated Test", "sequence_number": 2}
    
    # Test mit neuerer Sequenznummer (should resolve conflict)
    result = handle_todo_conflict(todo_id, existing_todo, incoming_todo, mock_db)
    assert result == True

def test_apply_lww_resolution():
    """Test LWW Resolution with different sequence numbers"""
    # Mock-Datenbank
    mock_db = Mock()
    
    # Testdaten für konflikte
    conflict_data = {
        "todo_id": 1,
        "incoming_data": {"id": 1, "title": "New Title", "sequence_number": 3},
        "existing_data": {"id": 1, "title": "Old Title", "sequence_number": 2}
    }
    
    # Test mit höherer Sequenznummer
    result = apply_lww_resolution(conflict_data["todo_id"], conflict_data["existing_data"], 
                                 conflict_data["incoming_data"], mock_db)
    assert result == True

def test_resolve_conflict():
    """Test Konfliktlösung"""
    mock_db = Mock()
    
    # Test mit gültigen Daten
    result = resolve_conflict(1, {"title": "Resolved Title", "sequence_number": 4})
    assert result == True
    
def test_get_conflict_logs_for_todo():
    """Test Konflikt-Logs abrufen"""
    mock_db = Mock()
    mock_db.execute.return_value.fetchall.return_value = []
    
    result = get_conflict_logs_for_todo(1, 50)
    assert isinstance(result, list)

def test_get_latest_conflict_resolution():
    """Test letzte Konflikt-Auflösung abrufen"""
    mock_db = Mock()
    
    result = get_latest_conflict_resolution(1)
    assert result is None or isinstance(result, dict)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])