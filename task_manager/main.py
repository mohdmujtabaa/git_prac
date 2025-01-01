from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_engine, Base, async_session_factory
from crud import create_task, read_task, update_task, delete_task, read_tasks
from schemas import TaskCreate, TaskRead, TaskUpdate
from typing import List, AsyncGenerator

app = FastAPI()

# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

# Create database tables
@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/tasks/", response_model=List[TaskRead])
async def api_read_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await read_tasks(db)
    return tasks


# Create a task
@app.post("/tasks/", response_model=TaskRead)
async def api_create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await create_task(task, db)

# Read a task by ID
@app.get("/tasks/{task_id}", response_model=TaskRead)
async def api_read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await read_task(task_id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update a task by ID
@app.put("/tasks/{task_id}", response_model=TaskRead)
async def api_update_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db)):
    updated_task = await update_task(task_id, task, db)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# Delete a task by ID
@app.delete("/tasks/{task_id}")
async def api_delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await delete_task(task_id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}


# Run the server with the command below
#uvicorn main:app --port 8001 --reload

