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


def test_create_and_get_user(client):
    response = client.post(
        "/users/",
        json={"name": "RouterUser", "email": "router@example.com"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "RouterUser"

    list_response = client.get("/users/")
    assert list_response.status_code == 200
    users = list_response.json()
    assert len(users) == 1
    assert users[0]["email"] == "router@example.com"


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404


def test_update_user(client):
    creation = client.post(
        "/users/",
        json={"name": "Before", "email": "before@example.com"},
    )
    user_id = creation.json()["id"]

    update = client.put(
        f"/users/{user_id}",
        json={"name": "After"},
    )
    assert update.status_code == 200
    assert update.json()["name"] == "After"


def test_delete_user(client):
    creation = client.post(
        "/users/",
        json={"name": "Delete", "email": "delete@example.com"},
    )
    user_id = creation.json()["id"]

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "User deleted Successfully"}

    follow_up = client.get(f"/users/{user_id}")
    assert follow_up.status_code == 404


def test_create_user_name_too_long(client):
    response = client.post(
        "/users/",
        json={"name": "A" * 101, "email": "long-name@example.com"},
    )
    assert response.status_code == 422
