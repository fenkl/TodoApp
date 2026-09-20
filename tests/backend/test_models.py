import pytest
from backend.models import Todo, TodoCreate, TodoUpdate

# Test für Todo Model
def test_todo_model():
    todo = Todo(id=1, title="Test Todo", completed=False, sequence_number=1)
    assert todo.id == 1
    assert todo.title == "Test Todo"
    assert todo.completed is False
    assert todo.sequence_number == 1

# Test für TodoCreate Model
def test_todo_create_model():
    todo_create = TodoCreate(title="Test Todo", completed=False)
    assert todo_create.title == "Test Todo"
    assert todo_create.completed is False

# Test für TodoUpdate Model
def test_todo_update_model():
    todo_update = TodoUpdate(title="Updated Todo", completed=True)
    assert todo_update.title == "Updated Todo"
    assert todo_update.completed is True

# Test mit optionalen Feldern
def test_todo_update_optional_fields():
    todo_update = TodoUpdate()
    assert todo_update.title is None
    assert todo_update.completed is None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])