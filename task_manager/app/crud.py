import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger("TaskAPI")

# Create a new task
async def create_task(task_data: TaskCreate, db: AsyncSession):
    try:
        new_task = Task(**task_data.model_dump())
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        logger.info(f"Task created with ID: {new_task.id}")
        return new_task
    except SQLAlchemyError as e:
        logger.error(f"Error creating task: {e}")
        await db.rollback()
        raise e

# Read all tasks
async def read_tasks(db: AsyncSession):
    try:
        query = select(Task)
        result = await db.execute(query)
        tasks = result.scalars().all()
        logger.info("Fetched all tasks.")
        return tasks
    except SQLAlchemyError as e:
        logger.error(f"Error fetching tasks: {e}")
        raise e  

# Read a task by ID
async def read_task(task_id: int, db: AsyncSession):
    try:
        query = select(Task).where(Task.id == task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()
        if task is None:
            logger.error(f"Task with ID {task_id} not found")
            return None
        else:
            logger.info(f"Fetched task with ID: {task_id}")
            return task
    except SQLAlchemyError as e:
        logger.error(f"Error fetching task: {e}")
        raise e

# Update a task by ID
async def update_task(task_id: int, task_data: TaskUpdate, db: AsyncSession) -> Optional[Task]:
    try:
        query = select(Task).where(Task.id == task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()
        if task is None:
            logger.warning(f"Task with ID {task_id} not found.")
            return None
        # Update the task
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        task.modified_at = datetime.now(timezone.utc)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        logger.info(f"Task with ID {task_id} updated successfully.")
        updated_task = await read_task(task_id, db)
        return updated_task
    except SQLAlchemyError as e:
        logger.error(f"Error updating task: {e}")
        await db.rollback()
        raise e

# Delete a task by ID
async def delete_task(task_id: int, db: AsyncSession) -> bool:
    try:
        query = select(Task).where(Task.id == task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()
        if task is None:
            logger.warning(f"Task with ID {task_id} not found.")
            return False
        else:
            query = delete(Task).where(Task.id == task_id)
            await db.execute(query)
            await db.commit()
            logger.info(f"Task with ID {task_id} deleted successfully.")
            return True
    except SQLAlchemyError as e:
        logger.error(f"Error deleting task: {e}")
        raise e