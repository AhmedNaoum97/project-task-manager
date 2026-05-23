import pytest
import json
from app import create_app, db
from app.models import User


@pytest.fixture
def client():
    """Create app for testing"""
    import os
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["JWT_SECRET"] = "test-secret-key"

    app = create_app()
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
        "password": "password123"
    })

    response = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "password123"
    })

    data = json.loads(response.data)
    return data["data"]["token"]


def test_signup(client):
    """Test user signup"""
    response = client.post("/api/v1/auth/signup", json={
        "email": "test@test.com",
        "password": "password123"
    })

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["success"] == True
    assert data["data"]["user"]["email"] == "test@test.com"


def test_login(client):
    """Test user login"""
    client.post("/api/v1/auth/signup", json={
        "email": "test@test.com",
        "password": "password123"
    })

    response = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "password123"
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