from typing import Optional
from pydantic import BaseModel

# Schema for creating a task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Schema for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Schema for reading a task
class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    class Config:
        orm_mode = True