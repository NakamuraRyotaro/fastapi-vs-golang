import pytest
from fastapi import HTTPException, status

from app.schemas.user_schema import UserCreate, UserUpdate
from app.services.user_service import UserService


@pytest.fixture
def sample_user(db_session):
    return UserService.create_user(
        db_session,
        UserCreate(name="Diana", email="diana@example.com"),
    )


def test_get_all_users(db_session, sample_user):
    users = UserService.get_all_users(db_session)
    assert len(users) == 1
    assert users[0].email == "diana@example.com"


def test_get_user_by_id(db_session, sample_user):
    user = UserService.get_user_by_id(db_session, sample_user.id)
    assert user.id == sample_user.id


def test_get_user_by_id_not_found(db_session):
    with pytest.raises(HTTPException) as exc:
        UserService.get_user_by_id(db_session, 999)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


def test_create_user_duplicate_email(db_session, sample_user):
    with pytest.raises(HTTPException) as exc:
        UserService.create_user(
            db_session,
            UserCreate(name="Dup", email="diana@example.com"),
        )
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


def test_update_user(db_session, sample_user):
    updated = UserService.update_user(
        db_session,
        sample_user.id,
        UserUpdate(name="Diana Updated"),
    )
    assert updated.name == "Diana Updated"


def test_update_user_not_found(db_session):
    with pytest.raises(HTTPException) as exc:
        UserService.update_user(db_session, 999, UserUpdate(name="Ghost"))
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user(db_session, sample_user):
    response = UserService.delete_user(db_session, sample_user.id)
    assert response == {"message": "User deleted Successfully"}


def test_delete_user_not_found(db_session):
    with pytest.raises(HTTPException) as exc:
        UserService.delete_user(db_session, 999)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
