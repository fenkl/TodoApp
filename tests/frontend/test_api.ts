import { fetchTodos, createTodo, updateTodo, deleteTodo } from '../../src/lib/api';

// Mock für fetch
global.fetch = jest.fn();

describe('API Functions', () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockReset();
  });

  test('should fetch todos successfully', async () => {
    const mockTodos = [
      { id: 1, title: 'Todo 1', completed: false },
      { id: 2, title: 'Todo 2', completed: true }
    ];
    
    (global.fetch as jest.Mock).mockImplementation(() => Promise.resolve({
      ok: true,
      json: () => Promise.resolve(mockTodos)
    }));
    
    const todos = await fetchTodos();
    expect(todos).toEqual(mockTodos);
    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/todos');
  });

  test('should create todo successfully', async () => {
    const newTodo = { id: 1, title: 'New Todo', completed: false };
    
    (global.fetch as jest.Mock).mockImplementation(() => Promise.resolve({
      ok: true,
      json: () => Promise.resolve(newTodo)
    }));
    
    const result = await createTodo({ title: 'New Todo', completed: false });
    expect(result).toEqual(newTodo);
    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/todos', expect.any(Object));
  });

  test('should update todo successfully', async () => {
    const updatedTodo = { id: 1, title: 'Updated Todo', completed: true };
    
    (global.fetch as jest.Mock).mockImplementation(() => Promise.resolve({
      ok: true,
      json: () => Promise.resolve(updatedTodo)
    }));
    
    const result = await updateTodo(1, { title: 'Updated Todo', completed: true });
    expect(result).toEqual(updatedTodo);
  });

  test('should delete todo successfully', async () => {
    const deletedTodo = { id: 1, title: 'Deleted Todo', completed: false };
    
    (global.fetch as jest.Mock).mockImplementation(() => Promise.resolve({
      ok: true,
      json: () => Promise.resolve(deletedTodo)
    }));
    
    const result = await deleteTodo(1);
    expect(result).toEqual(deletedTodo);
  });

  test('should handle fetch errors', async () => {
    (global.fetch as jest.Mock).mockImplementation(() => Promise.reject(new Error('Network error')));
    
    try {
      await fetchTodos();
      fail('Should have thrown an error');
    } catch (error) {
      expect(error.message).toBe('Network error');
    }
  });

  test('should handle HTTP errors', async () => {
    (global.fetch as jest.Mock).mockImplementation(() => Promise.resolve({
      ok: false,
      status: 404,
      statusText: 'Not Found'
    }));
    
    try {
      await fetchTodos();
      fail('Should have thrown an error');
    } catch (error) {
      expect(error.message).toContain('HTTP Error');
    }
  });

  test('should handle empty responses', async () => {
    (global.fetch as jest.Mock).mockImplementation(() => Promise.resolve({
      ok: true,
      json: () => Promise.resolve([])
    }));
    
    const todos = await fetchTodos();
    expect(todos).toEqual([]);
  });

  test('should handle undefined responses', async () => {
    (global.fetch as jest.Mock).mockImplementation(() => Promise.resolve({
      ok: true,
      json: () => Promise.resolve(undefined)
    }));
    
    const todos = await fetchTodos();
    expect(todos).toBeUndefined();
  });
});