// Prevents crashes from missing UI elements on macOS
#![cfg_attr(macos, feature(cocoa_file_dialog))]

mod todo_sync;

use tauri::Manager;
use todo_sync::{TodoSync, TodoSyncError};

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // Initialize the Todo Sync system
            let todo_sync = TodoSync::new();
            
            // Store in app state for access across handlers
            app.manage(todo_sync);
            
            #[cfg(debug_assertions)]
            {
                // Enable devtools in debug mode
                tauri::WebviewWindow::builder(app, "main".to_string(), tauri::WebviewUrl::External("http://localhost:3000".parse().unwrap()))
                    .title("Todo Sync App")
                    .width(800.0)
                    .height(600.0)
                    .build()
                    .expect("Failed to build webview window");
            }
            
            #[cfg(not(debug_assertions))]
            {
                // Create production window
                tauri::WebviewWindow::builder(app, "main".to_string(), tauri::WebviewUrl::App("index.html".parse().unwrap()))
                    .title("Todo Sync App")
                    .width(800.0)
                    .height(600.0)
                    .build()
                    .expect("Failed to build webview window");
            }
            
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("Error running Tauri application");
}