import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.models import user, todo  # noqa: F401 ensure metadata registration
from main import app

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def client():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def create_user(client):
    response = client.post(
        "/users/",
        json={"name": "TodoOwner", "email": "todo-owner@example.com"},
    )
    return response.json()["id"]


def test_create_and_get_todo(client):
    user_id = create_user(client)

    create_response = client.post(
        "/todos/",
        json={
            "title": "Write router tests",
            "description": "cover todo endpoints",
            "user_id": user_id,
        },
    )
    assert create_response.status_code == 201
    todo = create_response.json()
    assert todo["title"] == "Write router tests"

    list_response = client.get("/todos/")
    assert list_response.status_code == 200
    todos = list_response.json()
    assert len(todos) == 1
    assert todos[0]["user_id"] == user_id


def test_get_todo_not_found(client):
    response = client.get("/todos/999")
    assert response.status_code == 404


def test_get_todos_by_user(client):
    user_id = create_user(client)
    client.post(
        "/todos/",
        json={"title": "Task1", "description": None, "user_id": user_id},
    )

    response = client.get(f"/todos/user/{user_id}")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Task1"


def test_update_todo(client):
    user_id = create_user(client)
    todo_id = client.post(
        "/todos/",
        json={"title": "Old", "description": None, "user_id": user_id},
    ).json()["id"]

    update_response = client.put(
        f"/todos/{todo_id}",
        json={"title": "Updated", "completed": True},
    )
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True


def test_delete_todo(client):
    user_id = create_user(client)
    todo_id = client.post(
        "/todos/",
        json={"title": "ToDelete", "description": None, "user_id": user_id},
    ).json()["id"]

    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Todo deleted successfully"}

    follow_up = client.get(f"/todos/{todo_id}")
    assert follow_up.status_code == 404


def test_create_todo_title_too_long(client):
    user_id = create_user(client)
    response = client.post(
        "/todos/",
        json={
            "title": "T" * 256,
            "description": "too long title",
            "user_id": user_id,
        },
    )
    assert response.status_code == 422


def test_create_todo_missing_user(client):
    response = client.post(
        "/todos/",
        json={
            "title": "Needs owner",
            "description": None,
            "user_id": 999,
        },
    )
    assert response.status_code == 404
