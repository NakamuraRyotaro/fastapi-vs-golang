import pytest

from app.repositories.todo_repository import TodoRepository
from app.repositories.user_repository import UserRepository
from app.schemas.todo_schema import TodoCreate, TodoUpdate
from app.schemas.user_schema import UserCreate
from app.models.todo import Todo


@pytest.fixture
def sample_user(db_session):
    user = UserRepository.create(
        db_session,
        UserCreate(name="Charlie", email="charlie@example.com"),
    )
    return user


@pytest.fixture
def sample_todo(db_session, sample_user):
    todo = TodoRepository.create(
        db_session,
        TodoCreate(
            title="Initial Todo",
            description="learn testing",
            user_id=sample_user.id,
        ),
    )
    return todo


def test_create_todo(db_session, sample_user):
    todo = TodoRepository.create(
        db_session,
        TodoCreate(
            title="Write tests",
            description="cover repository layer",
            user_id=sample_user.id,
        ),
    )

    persisted = db_session.query(Todo).filter_by(id=todo.id).one()
    assert persisted.title == "Write tests"
    assert persisted.completed is False


def test_get_all_todos(db_session, sample_todo):
    todos = TodoRepository.get_all(db_session)
    assert len(todos) == 1
    assert todos[0].title == "Initial Todo"


def test_get_todo_by_id(db_session, sample_todo):
    found = TodoRepository.get_by_id(db_session, sample_todo.id)
    assert found is not None
    assert found.id == sample_todo.id


def test_get_todos_by_user(db_session, sample_todo, sample_user):
    todos = TodoRepository.get_by_user(db_session, sample_user.id)
    assert len(todos) == 1
    assert todos[0].user_id == sample_user.id


def test_update_todo(db_session, sample_todo):
    update_payload = TodoUpdate(title="Updated", completed=True)
    updated = TodoRepository.update(db_session, sample_todo.id, update_payload)

    assert updated is not None
    assert updated.title == "Updated"
    assert updated.completed is True


def test_update_todo_not_found(db_session):
    update_payload = TodoUpdate(title="Ghost")
    updated = TodoRepository.update(db_session, 999, update_payload)
    assert updated is None


def test_delete_todo(db_session, sample_todo):
    deleted = TodoRepository.delete(db_session, sample_todo.id)
    assert deleted is True
    assert TodoRepository.get_by_id(db_session, sample_todo.id) is None


def test_delete_todo_not_found(db_session):
    deleted = TodoRepository.delete(db_session, 999)
    assert deleted is False
