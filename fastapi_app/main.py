# app/main.py
from fastapi import FastAPI
from app.routers import user_router, todo_router

app = FastAPI(title="FastAPI Todo App")

app.include_router(user_router.router)
app.include_router(todo_router.router)
