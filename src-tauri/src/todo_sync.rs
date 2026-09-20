use tauri::Manager;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Todo {
    pub id: i32,
    pub title: String,
    pub description: Option<String>,
    pub completed: bool,
    pub created_at: String,
    pub updated_at: String,
    pub sequence_number: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TodoOperation {
    pub operation: String, // create, update, delete
    pub todo: Todo,
    pub timestamp: String,
}

#[tauri::command]
pub fn handle_todo_operation(
    app: tauri::AppHandle,
    operation: TodoOperation,
) -> Result<(), String> {
    // Log the operation
    eprintln!("Handling TODO operation: {} for todo {}", operation.operation, operation.todo.title);
    
    // Check if notifications are enabled and should be triggered based on configuration
    // In a real implementation, we would get the notification config from app state
    
    match operation.operation.as_str() {
        "create" => {
            // Notify about new TODO creation
            let payload = crate::notification::TodoNotificationPayload::new(
                operation.todo.id.to_string(),
                operation.todo.title.clone(),
                operation.todo.description.clone().unwrap_or_default(),
                "created".to_string()
            );
            // Call the notification function with the app handle
            if let Err(e) = crate::notification::show_notification(app, payload) {
                eprintln!("Notification failed: {}", e);
            }
        },
        "update" => {
            // Notify about TODO update  
            let payload = crate::notification::TodoNotificationPayload::new(
                operation.todo.id.to_string(),
                operation.todo.title.clone(),
                operation.todo.description.clone().unwrap_or_default(),
                "updated".to_string()
            );
            if let Err(e) = crate::notification::show_notification(app, payload) {
                eprintln!("Notification failed: {}", e);
            }
        },
        "delete" => {
            // Notify about TODO deletion
            let payload = crate::notification::TodoNotificationPayload::new(
                operation.todo.id.to_string(),
                operation.todo.title.clone(),
                operation.todo.description.clone().unwrap_or_default(),
                "deleted".to_string()
            );
            if let Err(e) = crate::notification::show_notification(app, payload) {
                eprintln!("Notification failed: {}", e);
            }
        },
        _ => {
            eprintln!("Unknown operation type: {}", operation.operation);
        }
    }
    
    Ok(())
}