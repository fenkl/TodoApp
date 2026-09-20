// Prevents IDE from complaining about unused imports
#![cfg_attr(miri, miri_no_feature)
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;
mod notification;
mod todo_sync;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, notification::show_notification, notification::setup_notification_config, todo_sync::handle_todo_operation])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}