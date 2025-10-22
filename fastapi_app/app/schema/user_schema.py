from datetime import datetime
from turtle import update
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    create_at: datetime
    update_at: datetime

    class Config:
        from_attribute = True # ORMオブジェクトが来たら、pydanticへ変換