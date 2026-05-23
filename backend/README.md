# Task Manager API

A full-stack task management application with authentication and AI-powered task analysis.

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

### Environment Variables

Create `.env` file:
```
DATABASE_URL=sqlite:///taskmanager.db
JWT_SECRET=your-secret-key-here
FLASK_ENV=development
CLAUDE_API_KEY=sk-your-key-here
```

### Run

```bash
python run.py
```

API will be available at `http://127.0.0.1:5000`

### Run Tests

```bash
pytest tests/ -v
```

---

## API Endpoints

### Authentication

**POST** `/api/v1/auth/signup`
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
Response: `201 Created` with user and JWT token

**POST** `/api/v1/auth/login`
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
Response: `200 OK` with JWT token

### Tasks

All task endpoints require JWT token in header:

```
Authorization: Bearer <token>
```

**POST** `/api/v1/tasks` - Create task
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high",
  "due_date": "2026-05-30T10:00:00"
}
```

**GET** `/api/v1/tasks` - Get all tasks
Query params: `?status=pending&priority=high`

**GET** `/api/v1/tasks/{id}` - Get single task

**PUT** `/api/v1/tasks/{id}` - Update task
```json
{
  "title": "Updated title",
  "status": "completed"
}
```

**DELETE** `/api/v1/tasks/{id}` - Delete task

### Health

**GET** `/api/v1/health` - Check API status

---

## Tech Stack

- **Backend:** Flask, SQLAlchemy, SQLite
- **Auth:** JWT, bcrypt
- **Testing:** pytest
- **Deployment:** Docker, Heroku

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   └── routes/
│       ├── auth.py
│       └── tasks.py
├── tests/
│   └── test_auth.py
├── run.py
└── requirements.txt
```
---

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Current test coverage:
- Authentication (signup, login)
- Task CRUD operations
- Protected routes
- Health check

---

## Next Steps

- [ ] Frontend (React + TypeScript)
- [ ] AD Mode (Claude AI integration/possibly Google Gemini)
- [ ] Docker containerization
- [ ] Heroku deployment