#!/usr/bin/env python3
"""
Smoke test for Todo Sync API
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://192.168.2.2:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            return True
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check failed with error: {e}")
        return False

def test_todo_crud():
    """Test CRUD operations for todos"""
    print("Testing todo CRUD operations...")
    
    # Test create
    print("Creating a new todo...")
    new_todo = {
        "title": "Test Todo",
        "description": "This is a test todo item",
        "completed": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/todos", json=new_todo)
        if response.status_code == 200:
            created_todo = response.json()
            print(f"✓ Todo created with ID: {created_todo['id']}")
            
            # Test read
            print("Reading the created todo...")
            response = requests.get(f"{BASE_URL}/api/v1/todos/{created_todo['id']}")
            if response.status_code == 200:
                retrieved_todo = response.json()
                print(f"✓ Todo retrieved: {retrieved_todo['title']}")
                
                # Test update
                print("Updating the todo...")
                update_data = {
                    "title": "Updated Test Todo",
                    "completed": True
                }
                response = requests.put(f"{BASE_URL}/api/v1/todos/{created_todo['id']}", json=update_data)
                if response.status_code == 200:
                    updated_todo = response.json()
                    print(f"✓ Todo updated: {updated_todo['title']}")
                    
                    # Test delete
                    print("Deleting the todo...")
                    response = requests.delete(f"{BASE_URL}/api/v1/todos/{created_todo['id']}")
                    if response.status_code == 200:
                        print("✓ Todo deleted successfully")
                        return True
                    else:
                        print(f"✗ Failed to delete todo, status: {response.status_code}")
                else:
                    print(f"✗ Failed to update todo, status: {response.status_code}")
            else:
                print(f"✗ Failed to retrieve todo, status: {response.status_code}")
        else:
            print(f"✗ Failed to create todo, status: {response.status_code}")
    except Exception as e:
        print(f"✗ Todo CRUD test failed with error: {e}")
        return False
    
    return False

def main():
    """Run all smoke tests"""
    print("Running smoke tests for Todo Sync API...")
    print("=" * 50)
    
    success = True
    success &= test_health()
    print()
    success &= test_todo_crud()
    
    print("=" * 50)
    if success:
        print("✓ All smoke tests passed!")
    else:
        print("✗ Some smoke tests failed!")
    
    return success

if __name__ == "__main__":
    main()