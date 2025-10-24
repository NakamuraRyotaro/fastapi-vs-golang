# app/services/todo_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo_schema import TodoCreate, TodoUpdate
from app.repositories.user_repository import UserRepository


class TodoService:

    @staticmethod
    def get_all_todos(db: Session):
        return TodoRepository.get_all(db)

    @staticmethod
    def get_todo_by_id(db: Session, todo_id: int):
        todo = TodoRepository.get_by_id(db, todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {todo_id} not found"
            )
        return todo

    @staticmethod
    def get_todos_by_user(db: Session, user_id: int):
        return TodoRepository.get_by_user(db, user_id)

    @staticmethod
    def create_todo(db: Session, todo_create: TodoCreate):
        if not UserRepository.get_by_id(db, todo_create.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {todo_create.user_id} is not found"
            )
        try:
            return TodoRepository.create(db, todo_create)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todo violates database constraints"
            ) from exc
        except SQLAlchemyError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid todo payload"
            ) from exc

    @staticmethod
    def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate):
        try:
            todo = TodoRepository.update(db, todo_id, todo_update)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todo violates database constraints"
            ) from exc
        except SQLAlchemyError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid todo payload"
            ) from exc
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {todo_id} not found"
            )
        return todo

    @staticmethod
    def delete_todo(db: Session, todo_id: int):
        try:
            deleted = TodoRepository.delete(db, todo_id)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to delete todo due to related data"
            ) from exc
        except SQLAlchemyError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid todo payload"
            ) from exc
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {todo_id} not found"
            )
        return {"message": "Todo deleted successfully"}
