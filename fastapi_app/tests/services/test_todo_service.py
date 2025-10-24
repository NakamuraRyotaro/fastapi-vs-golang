import pytest
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.repositories.todo_repository import TodoRepository
from app.schemas.todo_schema import TodoCreate, TodoUpdate
from app.schemas.user_schema import UserCreate
from app.services.todo_service import TodoService
from app.services.user_service import UserService


@pytest.fixture
def sample_user(db_session):
    return UserService.create_user(
        db_session,
        UserCreate(name="Evan", email="evan@example.com"),
    )


@pytest.fixture
def sample_todo(db_session, sample_user):
    return TodoService.create_todo(
        db_session,
        TodoCreate(
            title="Write docs",
            description="prepare README",
            user_id=sample_user.id,
        ),
    )


def test_get_all_todos(db_session, sample_todo):
    todos = TodoService.get_all_todos(db_session)
    assert len(todos) == 1
    assert todos[0].title == "Write docs"


def test_get_todo_by_id(db_session, sample_todo):
    todo = TodoService.get_todo_by_id(db_session, sample_todo.id)
    assert todo.id == sample_todo.id


def test_get_todo_by_id_not_found(db_session):
    with pytest.raises(HTTPException) as exc:
        TodoService.get_todo_by_id(db_session, 999)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


def test_get_todos_by_user(db_session, sample_user, sample_todo):
    todos = TodoService.get_todos_by_user(db_session, sample_user.id)
    assert len(todos) == 1
    assert todos[0].user_id == sample_user.id


def test_update_todo(db_session, sample_todo):
    updated = TodoService.update_todo(
        db_session,
        sample_todo.id,
        TodoUpdate(title="Write docs updated", completed=True),
    )
    assert updated.title == "Write docs updated"
    assert updated.completed is True


def test_update_todo_not_found(db_session):
    with pytest.raises(HTTPException) as exc:
        TodoService.update_todo(db_session, 999, TodoUpdate(title="Ghost"))
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


def test_delete_todo(db_session, sample_todo):
    response = TodoService.delete_todo(db_session, sample_todo.id)
    assert response == {"message": "Todo deleted successfully"}


def test_delete_todo_not_found(db_session):
    with pytest.raises(HTTPException) as exc:
        TodoService.delete_todo(db_session, 999)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


def test_update_todo_handles_integrity_error(db_session, sample_todo, monkeypatch):
    def _raise_integrity_error(db, todo_id, todo_update):  # noqa: ARG001
        raise IntegrityError("stmt", {}, Exception("orig"))

    monkeypatch.setattr(TodoRepository, "update", _raise_integrity_error)

    with pytest.raises(HTTPException) as exc:
        TodoService.update_todo(
            db_session,
            sample_todo.id,
            TodoUpdate(title="Safe title"),
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
