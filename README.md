# Task Management API

A simple RESTful API for managing tasks built with FastAPI and SQLite.

## Features
- Create, read, update, and delete tasks
- Task status tracking (pending, in progress, done)
- Tasks ordered by creation date
- SQLite persistent storage
- Automatic API documentation via Swagger/OpenAPI

## Setup
1. Install dependencies:

bash
pip install fastapi uvicorn pytest sqlite3

2. Run the application:

bash
uvicorn main:app --reload

Endpoints
GET /tasks - List all tasks
GET /tasks/{id} - Get specific task
POST /tasks - Create new task
PUT /tasks/{id} - Update task
DELETE /tasks/{id} - Delete task

Testing
Run tests with:

bash
pytest test_main.py

API Documentation
Available at http://localhost:8000/docs when running locally


This implementation:
1. Uses FastAPI for modern Python API development
2. Implements all required endpoints with proper HTTP status codes
3. Uses SQLite for persistent storage
4. Includes bonus features:
   - Task status (pending/in progress/done)
   - Creation date tracking and ordering
5. Provides input validation with Pydantic
6. Includes automatic Swagger documentation
7. Has basic unit tests
8. Follows RESTful conventions
9. Uses proper error handling

To run locally:
1. Save the files
2. Install requirements: `pip install fastapi uvicorn pytest`
3. Run: `uvicorn main:app --reload`
4. Access at `http://localhost:8000/docs` for interactive docs

The code is organized, commented, and includes error handling for cases like non-existent tasks. The tests verify basic CRUD operations.
