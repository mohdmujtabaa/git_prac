from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from models import Task
from schemas import TaskCreate, TaskUpdate
from datetime import datetime, timezone
from typing import Optional

# Create a new task
async def create_task(task_data: TaskCreate, db: AsyncSession):
    new_task = Task(**task_data.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

# Read all tasks
async def read_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()

# Read a task by ID
async def read_task(task_id: int, db: AsyncSession):
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# Update a task by ID
async def update_task(task_id: int, task_data: TaskUpdate, db: AsyncSession) -> Optional[Task]:
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        return None
    # Update the task
    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    task.modified_at = datetime.now(timezone.utc)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    updated_task = await read_task(task_id, db)
    return updated_task

# Delete a task by ID
async def delete_task(task_id: int, db: AsyncSession) -> bool:
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        return False
    else:
        query = delete(Task).where(Task.id == task_id)
        await db.execute(query)
        await db.commit()
        return True
