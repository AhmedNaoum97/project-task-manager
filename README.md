# Task Manager

A full-stack task management application with JWT authentication, React frontend, and AI-powered ADHD Mode.

## Live Demo

_Coming soon — deploying to Heroku_

---

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

Create `backend/.env`:

```
DATABASE_URL=sqlite:///taskmanager.db
JWT_SECRET=your-secret-key-here
FLASK_ENV=development
CLAUDE_API_KEY=sk-your-key-here
```

```bash
python run.py
```

API available at `http://127.0.0.1:5000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`

### Run Tests

```bash
cd backend
pytest tests/ -v
```

---

## Features

- JWT authentication (signup, login, protected routes)
- Full task CRUD (create, read, update, delete)
- Filter tasks by status and priority
- Status cycling (Pending → In Progress → Completed)
- ADHD Mode — AI-powered task analysis via Claude API _(coming soon)_

---

## Tech Stack

| Layer      | Technology                            |
| ---------- | ------------------------------------- |
| Frontend   | React, TypeScript, Vite, Tailwind CSS |
| Backend    | Flask, SQLAlchemy, SQLite             |
| Auth       | JWT, bcrypt                           |
| Testing    | pytest                                |
| Deployment | Docker, Heroku _(pending)_            |

---

## Project Structure

```
ProjectTaskManager/
├── backend/
│   ├── app/
│   │   ├── models/        # User, Task
│   │   └── routes/        # auth, tasks
│   ├── tests/
│   └── requirements.txt
└── frontend/
    └── src/
        ├── components/    # TaskCard, TaskForm
        ├── pages/         # LoginPage, SignupPage, TasksPage
        ├── context/       # AuthContext
        ├── services/      # api.ts
        └── types/         # task.ts
```

---

## API Endpoints

### Auth

| Method | Endpoint              | Description             |
| ------ | --------------------- | ----------------------- |
| POST   | `/api/v1/auth/signup` | Register new user       |
| POST   | `/api/v1/auth/login`  | Login and get JWT token |

### Tasks _(JWT required)_

| Method | Endpoint             | Description     |
| ------ | -------------------- | --------------- |
| GET    | `/api/v1/tasks`      | Get all tasks   |
| POST   | `/api/v1/tasks`      | Create task     |
| GET    | `/api/v1/tasks/{id}` | Get single task |
| PUT    | `/api/v1/tasks/{id}` | Update task     |
| DELETE | `/api/v1/tasks/{id}` | Delete task     |

### Health

| Method | Endpoint         | Description      |
| ------ | ---------------- | ---------------- |
| GET    | `/api/v1/health` | API health check |

---

## Next Steps

- [ ] ADHD/Dopamine Mode (Claude API integration)
- [ ] Docker containerization
- [ ] Heroku deployment
