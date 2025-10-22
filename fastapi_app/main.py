from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Hello, World!",
        "app_name": os.getenv("APP_NAME"),
        "environment": os.getenv("APP_ENV"),
        "version": os.getenv("APP_VERSION")
        }