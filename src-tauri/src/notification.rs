use tauri::Manager;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NotificationConfig {
    pub enabled: bool,
    pub title_template: String,
    pub body_template: String,
    pub icon: Option<String>,
    pub sound: Option<String>,
    pub vibrate: bool,
    pub notify_on_create: bool,
    pub notify_on_update: bool,
    pub notify_on_delete: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TodoNotificationPayload {
    pub todo_id: String,
    pub title: String,
    pub description: String,
    pub operation: String, // create, update, delete
    pub timestamp: String,
}

impl TodoNotificationPayload {
    pub fn new(todo_id: String, title: String, description: String, operation: String) -> Self {
        Self {
            todo_id,
            title,
            description,
            operation,
            timestamp: chrono::Utc::now().to_rfc3339(),
        }
    }
}

#[tauri::command]
pub fn show_notification(
    app: tauri::AppHandle,
    payload: TodoNotificationPayload,
) -> Result<(), String> {
    // Use Tauri's notification API
    #[cfg(desktop)]
    {
        use tauri::api::notification::Notification;
        
        let message = format!("TODO {}: {} - {}", payload.operation, payload.title, payload.description);
        eprintln!("Sending notification: {}", message);
        
        Notification::new()
            .title(format!("TodoSync - {}", payload.operation))
            .body(message)
            .show()
            .map_err(|e| format!("Failed to send notification: {:?}", e))?;
    }

    #[cfg(android)]
    {
        // Android specific notifications would go here
        println!("Android notification for TODO {} ({})", payload.title, payload.operation);
        // In a real implementation, we would use Android Notification API
    }

    #[cfg(target_os = "ios")]
    {
        // iOS specific notifications would go here  
        println!("iOS notification for TODO {} ({})", payload.title, payload.operation);
        // In a real implementation, we would use iOS Notification API
    }

    Ok(())
}

#[tauri::command]
pub fn setup_notification_config(
    app: tauri::AppHandle,
    config: NotificationConfig,
) -> Result<(), String> {
    // For now, just log the configuration - in a real implementation
    // we would save this to a config file or state management
    println!("Setting up notification config: {:?}", config);
    
    // Store configuration in app state for later use
    app.manage(config);
    
    Ok(())
}