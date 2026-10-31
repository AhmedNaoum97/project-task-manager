# Task Manager

A full-stack task management application with JWT authentication, a React frontend, and Docker deployment — hardened after a self-conducted security review.

## Live Demo

- **Frontend:** https://project-task-manager-navy.vercel.app
- **Backend:** currently offline (hosting trial ended) — run locally with Docker, see below.

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

Create `backend/.env`:

```
DATABASE_URL=sqlite:///taskmanager.db
JWT_SECRET=<generate: python -c "import secrets; print(secrets.token_urlsafe(48))">
FLASK_ENV=development
CORS_ORIGINS=http://localhost:5173
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

18 tests: auth, task CRUD, input validation, rate limiting, CORS, secret enforcement, and cross-user access.

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

Hardened after a self-conducted security review. Every control below is covered by an automated test.

| Control             | Implementation                                  | Threat addressed                        |
| ------------------- | ----------------------------------------------- | --------------------------------------- |
| Input validation    | Pydantic schemas, `extra="forbid"`              | Malformed input, mass-assignment        |
| Password policy     | 12–128 chars, bcrypt hashing                    | Weak passwords, offline cracking        |
| Rate limiting       | 5/min login, 3/min signup (Flask-Limiter)       | Online brute force                      |
| Access control      | All queries scoped to user; cross-user → 404    | IDOR (OWASP A01)                        |
| CORS allowlist      | Origins from `CORS_ORIGINS` env var             | Cross-origin abuse from malicious sites |
| Secret enforcement  | App refuses to start if `JWT_SECRET` < 32 chars | Weak / missing signing key              |
| Email normalization | Trim + lowercase                                | Duplicate accounts                      |
| Error handling      | Generic 500s, no input echoed in 400s           | Information disclosure                  |
| Login responses     | Identical message for wrong email/password      | Username enumeration                    |

### Known limitations

- Rate limiter uses in-memory storage (single instance only).
- Behind a reverse proxy, client IP requires `ProxyFix`.
- Signup returns 409 for existing emails (accepted enumeration trade-off, mitigated by rate limiting).
- JWT stored in `localStorage` (XSS would expose it).

---

## Tech Stack

| Layer      | Technology                            |
| ---------- | ------------------------------------- |
| Frontend   | React, TypeScript, Vite, Tailwind CSS |
| Backend    | Flask, SQLAlchemy, SQLite, gunicorn   |
| Validation | Pydantic                              |
| Auth       | JWT, bcrypt, Flask-Limiter            |
| Testing    | pytest                                |
| Deployment | Docker, nginx, Vercel                 |

---

## Project Structure

```
ProjectTaskManager/
├── backend/
│   ├── app/
│   │   ├── models/        # User, Task
│   │   ├── routes/        # auth, tasks
│   │   └── schemas.py     # Pydantic request validation
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

| Method | Endpoint            | Description             | Rate limit |
| ------ | ------------------- | ----------------------- | ---------- |
| POST   | /api/v1/auth/signup | Register new user       | 3/min      |
| POST   | /api/v1/auth/login  | Login and get JWT token | 5/min      |

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

---

## Docker

Create `backend/.env` first (see above), then:

```bash
docker-compose up
```

App available at `http://localhost`
