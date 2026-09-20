<script lang="ts">
  import { onMount } from 'svelte';
  import type { ConflictLog } from '../lib/api.ts';

  let conflictLogs: ConflictLog[] = [];
  let loading = true;
  let error: string | null = null;

  async function fetchConflictLogs() {
    try {
      loading = true;
      // In a real implementation, this would call the API
      // const logs = await fetchConflictLogs();
      // conflictLogs = logs.slice(0, 50);
      
      // For now, creating mock data as a placeholder
      conflictLogs = [
        {
          id: '1',
          todo_id: 'todo-1',
          winner: 'Android App',
          loser: 'Linux App',
          timestamp: new Date().toISOString()
        },
        {
          id: '2',
          todo_id: 'todo-2',
          winner: 'Linux App',
          loser: 'Android App',
          timestamp: new Date(Date.now() - 3600000).toISOString()
        }
      ];
    } catch (err) {
      error = 'Failed to load conflict logs';
      console.error(err);
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    fetchConflictLogs();
  });
</script>

<div class="conflict-log-panel">
  <h2>Conflict Log</h2>
  
  {#if loading}
    <p>Loading...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if conflictLogs.length === 0}
    <p>No conflicts found</p>
  {:else}
    <div class="log-list">
      {#each conflictLogs.slice(0, 50) as log (log.id)}
        <div class="log-entry">
          <div class="log-header">
            <span class="todo-id">Todo ID: {log.todo_id}</span>
            <span class="timestamp">{new Date(log.timestamp).toLocaleString()}</span>
          </div>
          <div class="log-content">
            <span class="winner">Winner: {log.winner}</span>
            <span class="loser">Loser: {log.loser}</span>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .conflict-log-panel {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 16px;
    margin: 16px 0;
    background-color: #f9f9f9;
  }

  .log-list {
    max-height: 400px;
    overflow-y: auto;
  }

  .log-entry {
    border-bottom: 1px solid #eee;
    padding: 8px 0;
  }

  .log-entry:last-child {
    border-bottom: none;
  }

  .log-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    font-weight: bold;
  }

  .log-content {
    display: flex;
    gap: 16px;
  }

  .winner {
    color: green;
  }

  .loser {
    color: red;
  }

  .error {
    color: red;
  }
</style>