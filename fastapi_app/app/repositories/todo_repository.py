from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.todo import Todo
from app.schemas.todo_schema import TodoCreate, TodoUpdate


class TodoRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Todo).all()
    
    @staticmethod
    def get_by_id(db: Session, todo_id: int):
        return db.query(Todo).filter(Todo.id == todo_id).first()
    
    @staticmethod
    def get_by_user(db: Session, user_id: int):
        return db.query(Todo).filter(Todo.user_id == user_id).all()
    
    @staticmethod
    def create(db: Session, todo_create: TodoCreate):
        new_todo = Todo(**todo_create.model_dump())
        db.add(new_todo)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        except SQLAlchemyError:
            db.rollback()
            raise
        db.refresh(new_todo)
        return new_todo
    
    @staticmethod
    def update(db: Session, todo_id: int, todo_update: TodoUpdate):
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return None
        for field, value in todo_update.model_dump(exclude_unset=True).items():
            setattr(todo, field, value)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        except SQLAlchemyError:
            db.rollback()
            raise
        db.refresh(todo)
        return todo
    
    @staticmethod
    def delete(db: Session, todo_id: int):
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return False

        db.delete(todo)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        except SQLAlchemyError:
            db.rollback()
            raise
        return True
