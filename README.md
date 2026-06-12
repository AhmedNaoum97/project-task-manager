# Task Manager

A full-stack task management application with JWT authentication, React frontend, and Docker deployment.

## Live Demo

- **Frontend:** https://project-task-manager-navy.vercel.app
- **Backend:** https://project-task-manager-production-a431.up.railway.app

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
python -m pytest tests/ -v
```

---

## Features

- JWT authentication (signup, login, protected routes)
- Full task CRUD (create, read, update, delete)
- Filter tasks by status and priority
- Status cycling (Pending → In Progress → Completed)
- Responsive dark UI with Tailwind CSS
- Dockerised for local full-stack development

---

## Security

- Passwords hashed with bcrypt; JWTs signed with a 256-bit secret stored in environment variables
- All task queries scoped to the authenticated user — cross-user access returns 404 (no resource disclosure)
- Generic error responses; full tracebacks logged server-side only
- Production served via gunicorn (debug mode gated behind FLASK_ENV)
- Identical error messages on login to prevent username enumeration

---

## Tech Stack

| Layer      | Technology                            |
| ---------- | ------------------------------------- |
| Frontend   | React, TypeScript, Vite, Tailwind CSS |
| Backend    | Flask, SQLAlchemy, SQLite, gunicorn   |
| Auth       | JWT, bcrypt                           |
| Testing    | pytest                                |
| Deployment | Docker, Railway, Vercel               |

---

## Project Structure

```
ProjectTaskManager/
├── backend/
│   ├── app/
│   │   ├── models/        # User, Task
│   │   └── routes/        # auth, tasks
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # TaskCard, TaskForm
│   │   ├── pages/         # LoginPage, SignupPage, TasksPage
│   │   ├── context/       # AuthContext
│   │   ├── services/      # api.ts
│   │   └── types/         # task.ts
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

---

## API Endpoints

### Auth

| Method | Endpoint            | Description             |
| ------ | ------------------- | ----------------------- |
| POST   | /api/v1/auth/signup | Register new user       |
| POST   | /api/v1/auth/login  | Login and get JWT token |

### Tasks (JWT required)

| Method | Endpoint           | Description     |
| ------ | ------------------ | --------------- |
| GET    | /api/v1/tasks      | Get all tasks   |
| POST   | /api/v1/tasks      | Create task     |
| GET    | /api/v1/tasks/{id} | Get single task |
| PUT    | /api/v1/tasks/{id} | Update task     |
| DELETE | /api/v1/tasks/{id} | Delete task     |

### Health

| Method | Endpoint       | Description      |
| ------ | -------------- | ---------------- |
| GET    | /api/v1/health | API health check |

## Docker

Run the full stack with one command:

```bash
docker-compose up
```

App available at `http://localhost`

---

## Roadmap

- ADHD/Dopamine Mode — AI-powered task prioritisation via Claude API
