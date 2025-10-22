from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str]
    compleated: bool = False

class TodoCreate(TodoBase):
    user_id : int

class TodoResponse(TodoBase):
    id: int
    user_id: int
    create_at: datetime
    update_at: datetime