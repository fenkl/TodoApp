use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};

// Error type for Todo Sync operations
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TodoSyncError {
    pub message: String,
    pub code: u32,
}

impl std::fmt::Display for TodoSyncError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "TodoSyncError [{}]: {}", self.code, self.message)
    }
}

impl std::error::Error for TodoSyncError {}

// Todo structure
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Todo {
    pub id: Option<i32>,
    pub title: String,
    pub description: Option<String>,
    pub completed: bool,
    pub created_at: String,
    pub updated_at: String,
}

// Conflict log entry
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConflictLog {
    pub id: Option<i32>,
    pub todo_id: i32,
    pub action: String,
    pub conflict_type: String,
    pub details: Option<String>,
    pub created_at: String,
}

// Sync message for WebSocket communication
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SyncMessage {
    pub r#type: String, // "updated", "created", "rejected"
    pub todo_id: i32,
    pub data: Option<Todo>,
}

// Main TodoSync manager
pub struct TodoSync {
    backend_url: String,
    connected: bool,
    websocket: Option<tokio_tungstenite::WebSocketStream<tokio::net::TcpStream>>,
    todos: HashMap<i32, Todo>,
    conflict_logs: Vec<ConflictLog>,
}

impl TodoSync {
    pub fn new() -> Self {
        Self {
            backend_url: "http://192.168.2.2:8000".to_string(),
            connected: false,
            websocket: None,
            todos: HashMap::new(),
            conflict_logs: Vec::new(),
        }
    }

    // Connect to the backend WebSocket
    pub async fn connect_websocket(&mut self) -> Result<(), TodoSyncError> {
        let url = format!("ws://{}/ws/sync", &self.backend_url.trim_start_matches("http://"));
        
        match tokio_tungstenite::connect_async(url).await {
            Ok((stream, _)) => {
                self.websocket = Some(stream);
                self.connected = true;
                Ok(())
            }
            Err(e) => Err(TodoSyncError {
                message: format!("WebSocket connection failed: {}", e),
                code: 1001,
            }),
        }
    }

    // Fetch all todos from backend
    pub async fn fetch_todos(&mut self) -> Result<Vec<Todo>, TodoSyncError> {
        let url = format!("{}/api/v1/todos", self.backend_url);
        
        match reqwest::get(&url).await {
            Ok(response) => {
                if response.status().is_success() {
                    let todos: Vec<Todo> = response.json().await.map_err(|e| TodoSyncError {
                        message: format!("Failed to parse todos: {}", e),
                        code: 1002,
                    })?;
                    
                    // Update local cache
                    self.todos.clear();
                    for todo in &todos {
                        if let Some(id) = todo.id {
                            self.todos.insert(id, todo.clone());
                        }
                    }
                    
                    Ok(todos)
                } else {
                    Err(TodoSyncError {
                        message: format!("Failed to fetch todos: {}", response.status()),
                        code: 1003,
                    })
                }
            }
            Err(e) => Err(TodoSyncError {
                message: format!("Network error fetching todos: {}", e),
                code: 1004,
            }),
        }
    }

    // Create a new todo
    pub async fn create_todo(&mut self, title: &str, description: Option<&str>) -> Result<Todo, TodoSyncError> {
        let url = format!("{}/api/v1/todos", self.backend_url);
        
        let todo_data = serde_json::json!({
            "title": title,
            "description": description,
            "completed": false
        });
        
        match reqwest::Client::new()
            .post(&url)
            .json(&todo_data)
            .send()
            .await
        {
            Ok(response) => {
                if response.status().is_success() {
                    let todo: Todo = response.json().await.map_err(|e| TodoSyncError {
                        message: format!("Failed to parse created todo: {}", e),
                        code: 1005,
                    })?;
                    
                    // Update local cache
                    if let Some(id) = todo.id {
                        self.todos.insert(id, todo.clone());
                    }
                    
                    Ok(todo)
                } else {
                    Err(TodoSyncError {
                        message: format!("Failed to create todo: {}", response.status()),
                        code: 1006,
                    })
                }
            }
            Err(e) => Err(TodoSyncError {
                message: format!("Network error creating todo: {}", e),
                code: 1007,
            }),
        }
    }

    // Update a todo
    pub async fn update_todo(&mut self, id: i32, title: Option<&str>, completed: Option<bool>) -> Result<Todo, TodoSyncError> {
        let url = format!("{}/api/v1/todos/{}", self.backend_url, id);
        
        let mut update_data = serde_json::Map::new();
        if let Some(t) = title {
            update_data.insert("title".to_string(), serde_json::Value::String(t.to_string()));
        }
        if let Some(c) = completed {
            update_data.insert("completed".to_string(), serde_json::Value::Bool(c));
        }
        
        match reqwest::Client::new()
            .put(&url)
            .json(&update_data)
            .send()
            .await
        {
            Ok(response) => {
                if response.status().is_success() {
                    let todo: Todo = response.json().await.map_err(|e| TodoSyncError {
                        message: format!("Failed to parse updated todo: {}", e),
                        code: 1008,
                    })?;
                    
                    // Update local cache
                    if let Some(cache_todo) = self.todos.get_mut(&id) {
                        cache_todo.updated_at = Self::get_current_timestamp();
                    }
                    self.todos.insert(id, todo.clone());
                    
                    Ok(todo)
                } else {
                    Err(TodoSyncError {
                        message: format!("Failed to update todo: {}", response.status()),
                        code: 1009,
                    })
                }
            }
            Err(e) => Err(TodoSyncError {
                message: format!("Network error updating todo: {}", e),
                code: 1010,
            }),
        }
    }

    // Delete a todo
    pub async fn delete_todo(&mut self, id: i32) -> Result<(), TodoSyncError> {
        let url = format!("{}/api/v1/todos/{}", self.backend_url, id);
        
        match reqwest::Client::new()
            .delete(&url)
            .send()
            .await
        {
            Ok(response) => {
                if response.status().is_success() {
                    // Remove from local cache
                    self.todos.remove(&id);
                    Ok(())
                } else {
                    Err(TodoSyncError {
                        message: format!("Failed to delete todo: {}", response.status()),
                        code: 1011,
                    })
                }
            }
            Err(e) => Err(TodoSyncError {
                message: format!("Network error deleting todo: {}", e),
                code: 1012,
            }),
        }
    }

    // Get conflict logs
    pub async fn fetch_conflict_logs(&mut self) -> Result<Vec<ConflictLog>, TodoSyncError> {
        let url = format!("{}/api/v1/conflict-logs", self.backend_url);
        
        match reqwest::get(&url).await {
            Ok(response) => {
                if response.status().is_success() {
                    let logs: Vec<ConflictLog> = response.json().await.map_err(|e| TodoSyncError {
                        message: format!("Failed to parse conflict logs: {}", e),
                        code: 1013,
                    })?;
                    
                    self.conflict_logs = logs.clone();
                    Ok(logs)
                } else {
                    Err(TodoSyncError {
                        message: format!("Failed to fetch conflict logs: {}", response.status()),
                        code: 1014,
                    })
                }
            }
            Err(e) => Err(TodoSyncError {
                message: format!("Network error fetching conflict logs: {}", e),
                code: 1015,
            }),
        }
    }

    // Get current timestamp
    fn get_current_timestamp() -> String {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards");
        
        now.as_secs().to_string()
    }

    // Check if connected
    pub fn is_connected(&self) -> bool {
        self.connected
    }
}