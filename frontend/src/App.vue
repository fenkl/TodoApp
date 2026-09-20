<template>
  <div class="app">
    <header class="app-header">
      <h1>Todo Sync App</h1>
      <p>Android Client - Synchronisiert mit Raspberry Pi Backend</p>
    </header>

    <main class="app-main">
      <section class="todo-section">
        <h2>Todos</h2>
        <div class="todo-controls">
          <input 
            v-model="newTodoTitle" 
            placeholder="Neue Aufgabe"
            @keyup.enter="createTodo"
          />
          <button @click="createTodo">Hinzufügen</button>
        </div>

        <div class="todo-list">
          <div 
            v-for="todo in todos" 
            :key="todo.id" 
            class="todo-item"
            :class="{ completed: todo.completed }"
          >
            <input 
              type="checkbox" 
              v-model="todo.completed"
              @change="updateTodo(todo)"
            />
            <span class="todo-text">{{ todo.title }}</span>
            <button @click="deleteTodo(todo.id)">Löschen</button>
          </div>
        </div>
      </section>

      <section class="conflict-section">
        <h2>Konfliktprotokoll</h2>
        <div class="conflict-list">
          <div 
            v-for="log in conflictLogs" 
            :key="log.id" 
            class="conflict-item"
          >
            <strong>Todo {{ log.todo_id }}:</strong> {{ log.action }} - {{ log.conflict_type }}
            <small>{{ log.created_at }}</small>
          </div>
        </div>
      </section>
    </main>

    <footer class="app-footer">
      <p>Status: {{ connectionStatus }}</p>
      <p>Synchronisiert mit: 192.168.2.2:8000</p>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';

export default {
  name: 'App',
  setup() {
    // State
    const todos = ref([]);
    const conflictLogs = ref([]);
    const newTodoTitle = ref('');
    const connectionStatus = ref('Verbindung herstellen...');
    
    // WebSocket connection
    let socket = null;
    
    // Fetch todos from backend
    const fetchTodos = async () => {
      try {
        const response = await fetch('http://192.168.2.2:8000/api/v1/todos');
        if (response.ok) {
          todos.value = await response.json();
        }
      } catch (error) {
        console.error('Fehler beim Laden der Todos:', error);
      }
    };
    
    // Fetch conflict logs from backend
    const fetchConflictLogs = async () => {
      try {
        const response = await fetch('http://192.168.2.2:8000/api/v1/conflict-logs');
        if (response.ok) {
          conflictLogs.value = await response.json();
        }
      } catch (error) {
        console.error('Fehler beim Laden der Konflikte:', error);
      }
    };
    
    // Create new todo
    const createTodo = async () => {
      if (!newTodoTitle.value.trim()) return;
      
      try {
        const response = await fetch('http://192.168.2.2:8000/api/v1/todos', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: newTodoTitle.value,
            description: '',
            completed: false
          })
        });
        
        if (response.ok) {
          const newTodo = await response.json();
          todos.value.unshift(newTodo);
          newTodoTitle.value = '';
        }
      } catch (error) {
        console.error('Fehler beim Erstellen des Todos:', error);
      }
    };
    
    // Update todo
    const updateTodo = async (todo) => {
      try {
        const response = await fetch(`http://192.168.2.2:8000/api/v1/todos/${todo.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: todo.title,
            description: todo.description,
            completed: todo.completed
          })
        });
        
        if (response.ok) {
          const updatedTodo = await response.json();
          const index = todos.value.findIndex(t => t.id === todo.id);
          if (index !== -1) {
            todos.value[index] = updatedTodo;
          }
        }
      } catch (error) {
        console.error('Fehler beim Aktualisieren des Todos:', error);
      }
    };
    
    // Delete todo
    const deleteTodo = async (id) => {
      try {
        const response = await fetch(`http://192.168.2.2:8000/api/v1/todos/${id}`, {
          method: 'DELETE'
        });
        
        if (response.ok) {
          todos.value = todos.value.filter(todo => todo.id !== id);
        }
      } catch (error) {
        console.error('Fehler beim Löschen des Todos:', error);
      }
    };
    
    // Connect to WebSocket
    const connectWebSocket = () => {
      try {
        socket = new WebSocket('ws://192.168.2.2:8000/ws/sync');
        
        socket.onopen = () => {
          connectionStatus.value = 'Verbunden';
          console.log('WebSocket verbunden');
        };
        
        socket.onmessage = (event) => {
          const message = JSON.parse(event.data);
          console.log('WebSocket Nachricht:', message);
          
          // Handle sync messages
          if (message.type === 'updated') {
            fetchTodos(); // Refresh todos on update
          } else if (message.type === 'created') {
            fetchTodos(); // Refresh todos on creation
          } else if (message.type === 'rejected') {
            // Handle conflict rejection
            console.log('Konflikt abgewiesen:', message);
            fetchConflictLogs();
          }
        };
        
        socket.onclose = () => {
          connectionStatus.value = 'Verbindung getrennt';
          console.log('WebSocket getrennt');
        };
        
        socket.onerror = (error) => {
          connectionStatus.value = 'Fehler';
          console.error('WebSocket Fehler:', error);
        };
      } catch (error) {
        console.error('Fehler beim Verbinden mit WebSocket:', error);
        connectionStatus.value = 'Verbindung fehlgeschlagen';
      }
    };
    
    // Cleanup
    const cleanup = () => {
      if (socket) {
        socket.close();
      }
    };
    
    // Lifecycle
    onMounted(() => {
      fetchTodos();
      fetchConflictLogs();
      connectWebSocket();
    });
    
    onUnmounted(() => {
      cleanup();
    });
    
    return {
      todos,
      conflictLogs,
      newTodoTitle,
      connectionStatus,
      createTodo,
      updateTodo,
      deleteTodo
    };
  }
}
</script>

<style>
.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.app-main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.todo-section, .conflict-section {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.todo-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.todo-controls input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.todo-controls button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.todo-item.completed .todo-text {
  text-decoration: line-through;
  color: #888;
}

.todo-item button {
  margin-left: auto;
  padding: 4px 8px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.conflict-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
  font-size: 0.9em;
}

.conflict-item small {
  display: block;
  color: #666;
  margin-top: 4px;
}

.app-footer {
  text-align: center;
  margin-top: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .app-main {
    grid-template-columns: 1fr;
  }
}
</style>