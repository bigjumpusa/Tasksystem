from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

app = FastAPI(title="Task Management API")

# Pydantic model for task input validation
class TaskCreate(BaseModel):
    title: str
    description: str
    status: Optional[str] = "pending"  # Default status

class Task(TaskCreate):
    id: int
    created_at: str

# Database initialization
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 description TEXT,
                 status TEXT,
                 created_at TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """List all tasks, ordered by creation date"""
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = [dict(row) for row in c.fetchall()]
    conn.close()
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()
    conn.close()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(task)

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task"""
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    created_at = datetime.now().isoformat()
    c.execute(
        "INSERT INTO tasks (title, description, status, created_at) VALUES (?, ?, ?, ?)",
        (task.title, task.description, task.status, created_at)
    )
    task_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {**task.dict(), "id": task_id, "created_at": created_at}

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskCreate):
    """Update an existing task"""
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",
        (task.title, task.description, task.status, task_id)
    )
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    c.execute("SELECT created_at FROM tasks WHERE id = ?", (task_id,))
    created_at = c.fetchone()[0]
    conn.commit()
    conn.close()
    
    return {**task.dict(), "id": task_id, "created_at": created_at}

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Delete a task"""
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    conn.commit()
    conn.close()

# Run with: uvicorn main:app --reload
