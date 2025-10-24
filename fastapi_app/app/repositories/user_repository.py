from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate

class UserRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()
    
    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create(db: Session, user_create: UserCreate):
        new_user = User(**user_create.model_dump())
        db.add(new_user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def update(db: Session, user_id: int, user_update: UserUpdate):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        return True