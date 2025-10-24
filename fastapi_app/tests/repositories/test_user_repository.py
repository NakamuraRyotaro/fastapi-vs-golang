import pytest

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate
from app.models.user import User


@pytest.fixture
def sample_user(db_session):
    user_create = UserCreate(name="Alice", email="alice@example.com")
    user = UserRepository.create(db_session, user_create)
    yield user


def test_create_user(db_session):
    user_create = UserCreate(name="Bob", email="bob@example.com")
    user = UserRepository.create(db_session, user_create)

    retrieved = db_session.query(User).filter_by(email="bob@example.com").one()
    assert user.id == retrieved.id
    assert retrieved.name == "Bob"


def test_get_all_users(db_session, sample_user):
    users = UserRepository.get_all(db_session)
    assert len(users) == 1
    assert users[0].email == "alice@example.com"


def test_get_user_by_id(db_session, sample_user):
    found = UserRepository.get_by_id(db_session, sample_user.id)
    assert found is not None
    assert found.id == sample_user.id


def test_get_user_by_email(db_session, sample_user):
    found = UserRepository.get_by_email(db_session, "alice@example.com")
    assert found is not None
    assert found.email == "alice@example.com"


def test_update_user(db_session, sample_user):
    update_payload = UserUpdate(name="Alice Updated")
    updated = UserRepository.update(db_session, sample_user.id, update_payload)

    assert updated is not None
    assert updated.name == "Alice Updated"


def test_update_user_not_found(db_session):
    update_payload = UserUpdate(name="Ghost")
    updated = UserRepository.update(db_session, 999, update_payload)
    assert updated is None


def test_delete_user(db_session, sample_user):
    deleted = UserRepository.delete(db_session, sample_user.id)
    assert deleted is True
    assert UserRepository.get_by_id(db_session, sample_user.id) is None


def test_delete_user_not_found(db_session):
    deleted = UserRepository.delete(db_session, 999)
    assert deleted is False
