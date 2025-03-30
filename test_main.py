import pytest
from fastapi.testclient import TestClient
from main import app, init_db
import sqlite3

@pytest.fixture
def client():
    # Reset database before each test
    conn = sqlite3.connect("tasks.db")
    conn.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
    return TestClient(app)

def test_create_and_get_task(client):
    # Test task creation
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 201
    task = response.json()
    assert task["title"] == "Test Task"
    assert task["status"] == "pending"
    
    # Test getting the created task
    task_id = task["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_update_and_delete_task(client):
    # Create a task first
    response = client.post(
        "/tasks",
        json={"title": "Initial", "description": "Desc"}
    )
    task_id = response.json()["id"]
    
    # Test update
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated", "description": "New Desc", "status": "done"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "done"
    
    # Test delete
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
