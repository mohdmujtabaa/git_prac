from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SqlAlchemyEnum
from app.database import Base
from enum import Enum
from datetime import datetime, timezone

class TaskStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SqlAlchemyEnum(TaskStatus), default=TaskStatus.NEW, nullable=False)
    assigned_to = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    modified_at = Column(DateTime, nullable=True)
