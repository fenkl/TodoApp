<script lang="ts">
  import { notificationManager } from '../lib/notification-config.ts';
  
  let settings = notificationManager.getSettings();
  let permissionGranted = false;
  
  async function requestPermission() {
    try {
      const granted = await notificationManager.requestPermission();
      permissionGranted = granted;
    } catch (error) {
      console.error('Failed to request notification permission:', error);
    }
  }
  
  function updateSetting(key: string, value: any) {
    settings[key] = value;
    notificationManager.updateSettings({ [key]: value });
  }
  
  function resetToDefault() {
    notificationManager.updateSettings(notificationManager.getSettings());
    settings = notificationManager.getSettings();
  }
</script>

<div class="notification-settings">
  <h2>Notification Settings</h2>
  
  <div class="setting-group">
    <label>
      <input 
        type="checkbox" 
        bind:checked={settings.enabled} 
        on:change={() => updateSetting('enabled', settings.enabled)}
      />
      Enable Notifications
    </label>
  </div>
  
  <div class="setting-group">
    <label>
      <input 
        type="checkbox" 
        bind:checked={settings.notifyOnCreate} 
        on:change={() => updateSetting('notifyOnCreate', settings.notifyOnCreate)}
        disabled={!settings.enabled}
      />
      Notify on Todo Creation
    </label>
  </div>
  
  <div class="setting-group">
    <label>
      <input 
        type="checkbox" 
        bind:checked={settings.notifyOnUpdate} 
        on:change={() => updateSetting('notifyOnUpdate', settings.notifyOnUpdate)}
        disabled={!settings.enabled}
      />
      Notify on Todo Update
    </label>
  </div>
  
  <div class="setting-group">
    <label>
      <input 
        type="checkbox" 
        bind:checked={settings.notifyOnDelete} 
        on:change={() => updateSetting('notifyOnDelete', settings.notifyOnDelete)}
        disabled={!settings.enabled}
      />
      Notify on Todo Deletion
    </label>
  </div>
  
  <div class="setting-group">
    <label>
      <input 
        type="checkbox" 
        bind:checked={settings.soundEnabled} 
        on:change={() => updateSetting('soundEnabled', settings.soundEnabled)}
        disabled={!settings.enabled}
      />
      Enable Sound Notifications
    </label>
  </div>
  
  <div class="setting-group">
    <label>
      <input 
        type="checkbox" 
        bind:checked={settings.vibrationEnabled} 
        on:change={() => updateSetting('vibrationEnabled', settings.vibrationEnabled)}
        disabled={!settings.enabled}
      />
      Enable Vibration
    </label>
  </div>
  
  <div class="setting-group">
    <button 
      on:click={requestPermission} 
      class="permission-button"
      disabled={permissionGranted}
    >
      {permissionGranted ? 'Permission Granted' : 'Request Notification Permission'}
    </button>
  </div>
  
  <div class="setting-group">
    <button 
      on:click={resetToDefault}
      class="reset-button"
    >
      Reset to Default
    </button>
  </div>
</div>

<style>
  .notification-settings {
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  .setting-group {
    margin-bottom: 15px;
  }

  .notification-settings h2 {
    margin-top: 0;
    color: #333;
  }

  .permission-button, .reset-button {
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 10px;
  }

  .permission-button:hover, .reset-button:hover {
    background-color: #0056b3;
  }

  .permission-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  label {
    display: flex;
    align-items: center;
    font-size: 14px;
  }

  input[type="checkbox"] {
    margin-right: 8px;
  }

  input[type="checkbox"]:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>