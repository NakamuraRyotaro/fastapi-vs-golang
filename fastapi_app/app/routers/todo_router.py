# app/routers/todo_router.py
from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.todo_schema import TodoResponse, TodoCreate, TodoUpdate
from app.services.todo_service import TodoService

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


@router.get("/", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return TodoService.get_all_todos(db)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    return TodoService.get_todo_by_id(db, todo_id)


@router.get("/user/{user_id}", response_model=List[TodoResponse])
def get_todos_by_user(user_id: int, db: Session = Depends(get_db)):
    return TodoService.get_todos_by_user(db, user_id)


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo_create: TodoCreate, db: Session = Depends(get_db)):
    return TodoService.create_todo(db, todo_create)


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    return TodoService.update_todo(db, todo_id, todo_update)


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    return TodoService.delete_todo(db, todo_id)
