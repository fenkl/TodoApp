<script lang="ts">
  import TodoList from './components/TodoList.svelte';
  import ConflictLogPanel from './components/ConflictLogPanel.svelte';
  import NotificationSettings from './components/NotificationSettings.svelte';
  import { onMount } from 'svelte';
  import { TodoWebSocket } from './lib/ws.ts';
  import { offlineQueue } from './lib/offline-queue.ts';
  import { notificationManager } from './lib/notification-config.ts';

  let isConnected = false;
  let connectionStatus = 'Disconnected';
  
  // Initialize WebSocket
  const ws = new TodoWebSocket('ws://192.168.2.2:8000');
  
  onMount(() => {
    // Handle websocket connection status
    ws.onOpen(() => {
      isConnected = true;
      connectionStatus = 'Connected';
      console.log('WebSocket connected');
      
      // Attempt to sync any offline actions when reconnected
      syncOfflineQueue();
    });
    
    ws.onClose(() => {
      isConnected = false;
      connectionStatus = 'Disconnected';
      console.log('WebSocket disconnected');
    });
    
    ws.onMessage((message) => {
      console.log('Received message:', message);
      // Handle incoming messages from the server
      try {
        const data = JSON.parse(message);
        if (data.type === 'todo_operation') {
          // Handle notifications for todo operations that come from the server
          console.log('Handling server operation:', data.operation);
        }
      } catch (e) {
        console.error('Error parsing websocket message:', e);
      }
    });
  });
  
  async function syncOfflineQueue() {
    try {
      console.log('Attempting to sync offline queue');
      // In a real implementation, this would actually call the API with the queued actions
      await offlineQueue.syncWithServer('http://192.168.2.2:8000/api/v1/todos');
    } catch (error) {
      console.error('Failed to sync offline queue:', error);
    }
  }
  
  // Clean up WebSocket on unmount
  function onDestroy() {
    ws.close();
  }
</script>

<div class="app-container">
  <header class="app-header">
    <h1>Todo Sync App</h1>
    <div class="connection-status">
      Status: 
      <span class="{isConnected ? 'connected' : 'disconnected'}">
        {connectionStatus}
      </span>
    </div>
  </header>
  
  <main class="app-main">
    <TodoList />
    <NotificationSettings />
    <ConflictLogPanel />
  </main>
</div>

<style>
  .app-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 1px solid #ddd;
  }
  
  .connection-status {
    font-weight: bold;
  }
  
  .connected {
    color: green;
  }
  
  .disconnected {
    color: red;
  }
  
  .app-main {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
</style>