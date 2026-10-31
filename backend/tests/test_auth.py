import pytest
import json
from app.models import User
from app import create_app, db, limiter

TEST_PASSWORD = "correct-horse-battery"


@pytest.fixture
def client():
    """Create app for testing"""
    import os
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["JWT_SECRET"] = "test-secret-key-that-is-at-least-32-bytes"
    app = create_app()
    limiter.reset()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def auth_token(client):
    """Get JWT token for testing protected routes"""
    client.post("/api/v1/auth/signup", json={
        "email": "test@test.com",
        "password": TEST_PASSWORD
    })

    response = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": TEST_PASSWORD
    })

    data = json.loads(response.data)
    return data["data"]["token"]


def test_signup(client):
    """Test user signup"""
    response = client.post("/api/v1/auth/signup", json={
        "email": "test@test.com",
        "password": TEST_PASSWORD
    })

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["success"] == True
    assert data["data"]["user"]["email"] == "test@test.com"


def test_login(client):
    """Test user login"""
    client.post("/api/v1/auth/signup", json={
        "email": "test@test.com",
        "password": TEST_PASSWORD
    })

    response = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": TEST_PASSWORD
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] == True
    assert "token" in data["data"]


def test_create_task(client, auth_token):
    """Test creating a task"""
    response = client.post("/api/v1/tasks",
                           json={
                               "title": "Test Task",
                               "description": "This is a test",
                               "priority": "high"
                           },
                           headers={"Authorization": f"Bearer {auth_token}"}
                           )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["success"] == True
    assert data["data"]["title"] == "Test Task"


def test_get_tasks(client, auth_token):
    """Test getting all tasks"""
    # Create a task first
    client.post(
        "/api/v1/tasks",
        json={"title": "Test Task"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] == True
    assert len(data["data"]) == 1


def test_create_task_requires_auth(client):
    """Test that creating a task requires authentication"""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task"}
    )

    assert response.status_code == 401


def test_health_check(client):
    """Test health endpoint"""
    response = client.get("/api/v1/health")
    data = json.loads(response.data)
    assert data["status"] == "ok"


def test_signup_weak_password(client):
    """Test that signup fails with a weak password"""
    response = client.post("/api/v1/auth/signup", json={
        "email": "test@test.com",
        "password": "weak"
    })
    assert response.status_code == 400


def test_signup_invalid_email(client):
    """Test that signup fails with an invalid e-mail"""
    response = client.post("/api/v1/auth/signup", json={
        "email": "invalid-email",
        "password": TEST_PASSWORD
    })
    assert response.status_code == 400


def test_create_task_invalid_date(client, auth_token):
    """Test that creating a task fails with an invalid date format"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "due_date": "nope"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400


def test_create_task_invalid_priority(client, auth_token):
    """Test that creating a task fails with an invalid priority"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "priority": "invalid"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400

def test_create_task_extra_field(client, auth_token):
    """Test that creating a task fails when an unknown field is sent"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "user_id": "someone-else"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400

def test_update_task_null_title(client, auth_token):
    """Test that updating a task fails when title is null"""
    # Create a task first
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    task_id = json.loads(create_response.data)["data"]["id"]

    # Try to set title to null
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": None},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 400

def test_signup_email_case_insensitive(client):
    """Same email with different case cannot register twice"""
    client.post("/api/v1/auth/signup", json={
        "email": "Test@Test.com",
        "password": TEST_PASSWORD
    })
    response = client.post("/api/v1/auth/signup", json={
        "email": "  test@test.com ",
        "password": TEST_PASSWORD
    })
    assert response.status_code == 409


def test_cors_blocks_unknown_origin(client):
    """Unknown origins get no CORS allow header"""
    response = client.get("/api/v1/health", headers={"Origin": "https://evil.com"})
    assert "Access-Control-Allow-Origin" not in response.headers

def test_app_refuses_weak_jwt_secret(monkeypatch):
    """App must not start with a short JWT secret"""
    monkeypatch.setenv("JWT_SECRET", "too-short")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    with pytest.raises(RuntimeError):
        create_app()

def test_login_rate_limited(client):
    """6th login attempt in a minute is blocked"""
    for _ in range(5):
        client.post("/api/v1/auth/login", json={
            "email": "test@test.com",
            "password": "wrong-password"
        })
    response = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "wrong-password"
    })
    assert response.status_code == 429