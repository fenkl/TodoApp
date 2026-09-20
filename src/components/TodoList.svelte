<script lang="ts">
  import { onMount } from 'svelte';
  import type { Todo } from '../lib/api.ts';
  import { offlineQueue } from '../lib/offline-queue.ts';
  import { TodoWebSocket } from '../lib/ws.ts';

  let todos: Todo[] = [];
  let newTodoTitle = '';
  let loading = false;
  let error: string | null = null;
  let ws: TodoWebSocket;

  // Initialize WebSocket connection
  onMount(() => {
    try {
      // Create WebSocket instance - assuming backend at localhost:8000
      ws = new TodoWebSocket('ws://localhost:8000');
      
      ws.onOpen(() => {
        console.log('WebSocket connected for todo operations');
      });
      
      ws.onClose(() => {
        console.log('WebSocket disconnected');
      });
      
      ws.onMessage((message) => {
        console.log('Received WebSocket message:', message);
        // Handle incoming messages from the server
        try {
          const data = JSON.parse(message);
          if (data.type === 'todo_update') {
            // Handle received todo updates (could refresh sync)
            console.log('Todo update received from server:', data);
          }
        } catch (e) {
          console.error('Error parsing WebSocket message:', e);
        }
      });
    } catch (err) {
      console.error('Error initializing WebSocket:', err);
    }
    
    fetchTodos();
  });

  async function fetchTodos() {
    try {
      loading = true;
      // In a real implementation, we would call api.fetchTodos()
      // For now, using mock data to demonstrate structure
      todos = [
        { id: '1', title: 'Learn Svelte', completed: false, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
        { id: '2', title: 'Build Todo App', completed: true, created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
      ];
    } catch (err) {
      error = 'Failed to load todos';
      console.error(err);
    } finally {
      loading = false;
    }
  }

  async function addTodo() {
    if (!newTodoTitle.trim()) return;

    const todo = {
      title: newTodoTitle.trim(),
      completed: false
    };

    try {
      // In a real scenario, we would call api.createTodo(todo) and handle offline syncing
      const newTodo: Todo = {
        ...todo,
        id: `todo-${Date.now()}`,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      todos = [newTodo, ...todos];
      newTodoTitle = '';

      // Queue the action for offline sync
      offlineQueue.addAction({
        id: `action-${Date.now()}`,
        type: 'create',
        data: newTodo,
        timestamp: Date.now()
      });

      // Also send to server via WebSocket immediately if connected
      if (ws && ws.isConnected()) {
        ws.sendTodoOperation('create', newTodo.id, newTodo);
      }

    } catch (err) {
      error = 'Failed to add todo';
      console.error(err);
    }
  }

  async function toggleTodo(id: string) {
    try {
      const todo = todos.find(t => t.id === id);
      if (!todo) return;

      const updatedTodo = { 
        ...todo, 
        completed: !todo.completed, 
        updated_at: new Date().toISOString() 
      };

      // Update local state
      todos = todos.map(t => t.id === id ? updatedTodo : t);

      // Queue the action for offline sync
      offlineQueue.addAction({
        id: `action-${Date.now()}`,
        type: 'update',
        data: updatedTodo,
        timestamp: Date.now()
      });

      // Also send to server via WebSocket immediately if connected
      if (ws && ws.isConnected()) {
        ws.sendTodoOperation('update', id, updatedTodo);
      }

    } catch (err) {
      error = 'Failed to update todo';
      console.error(err);
    }
  }

  async function deleteTodo(id: string) {
    try {
      todos = todos.filter(todo => todo.id !== id);

      // Queue the action for offline sync
      offlineQueue.addAction({
        id: `action-${Date.now()}`,
        type: 'delete',
        data: { id },
        timestamp: Date.now()
      });

      // Also send to server via WebSocket immediately if connected
      if (ws && ws.isConnected()) {
        ws.sendTodoOperation('delete', id, { id });
      }

    } catch (err) {
      error = 'Failed to delete todo';
      console.error(err);
    }
  }
</script>

<div class="todo-app">
  <h1>Todo List</h1>
  
  <form on:submit|preventDefault={addTodo} class="add-todo-form">
    <input 
      type="text" 
      bind:value={newTodoTitle} 
      placeholder="Add a new todo..."
      class="todo-input"
    >
    <button type="submit" class="add-button">Add</button>
  </form>

  {#if loading}
    <p>Loading todos...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if todos.length === 0}
    <p>No todos found</p>
  {:else}
    <ul class="todo-list">
      {#each todos as todo (todo.id)}
        <li class="todo-item {todo.completed ? 'completed' : ''}">
          <span 
            class="todo-text" 
            on:click={() => toggleTodo(todo.id)}
          >
            {todo.title}
          </span>
          <button 
            class="delete-button" 
            on:click={() => deleteTodo(todo.id)}
          >
            Delete
          </button>
        </li>
      {/each}
    </ul>
  {/if}
</div>

<style>
  .todo-app {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }

  .add-todo-form {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }

  .todo-input {
    flex: 1;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .add-button {
    padding: 8px 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .add-button:hover {
    background-color: #0056b3;
  }

  .todo-list {
    list-style-type: none;
    padding: 0;
  }

  .todo-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    border-bottom: 1px solid #eee;
  }

  .todo-item.completed .todo-text {
    text-decoration: line-through;
    color: #888;
  }

  .todo-text {
    flex: 1;
    cursor: pointer;
  }

  .delete-button {
    padding: 4px 8px;
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .delete-button:hover {
    background-color: #c82333;
  }

  .error {
    color: red;
    text-align: center;
  }
</style>