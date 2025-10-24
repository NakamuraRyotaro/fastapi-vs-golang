from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UserService:

    @staticmethod
    def get_all_users(db: Session):
        return UserRepository.get_all(db)
    
    @staticmethod
    def get_user_by_id(db:Session, user_id: int):
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user

    @staticmethod
    def create_user(db: Session, user_create: UserCreate):
        # 重複チェック
        existing = UserRepository.get_by_email(db, user_create.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        try:
            return UserRepository.create(db, user_create)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            ) from exc
    
    @staticmethod
    def update_user(db: Session, user_id, user_update: UserUpdate):
        try:
            user = UserRepository.update(db, user_id, user_update)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            ) from exc

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int):
        try: 
            deleted = UserRepository.delete(db, user_id)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User cannot be deleted due to related data"
            ) from exc
            
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return {"message": "User deleted Successfully"}