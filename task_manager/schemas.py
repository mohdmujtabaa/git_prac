from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from models import TaskStatus


# Schema for base task
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.NEW
    assigned_to: Optional[str] = None
    

# Schema for creating a task
class TaskCreate(TaskBase):
    pass

# Schema for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.NEW
    assigned_to: Optional[str] = None


# Schema for reading a task
class TaskRead(TaskBase):
    id: int
    created_at: datetime
    modified_at: Optional[datetime] = None

    class Config:
        orm_mode = True