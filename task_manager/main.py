import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_engine, Base, async_session_factory
from crud import create_task, read_task, update_task, delete_task, read_tasks
from schemas import TaskCreate, TaskRead, TaskUpdate
from typing import List, AsyncGenerator
from logging.config import dictConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(),
              logging.FileHandler("task_api.log"),
              ],
)

app = FastAPI()

# Define a logger for your application
logger = logging.getLogger("TaskAPI")

# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

# Create database tables
@app.on_event("startup")
async def startup():
    logger.info("Starting Task API ...") 
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Task API...")

@app.get("/tasks/", response_model=List[TaskRead])
async def api_read_tasks(db: AsyncSession = Depends(get_db)):
    logger.info("GET /tasks/ endpoint called.")
    tasks = await read_tasks(db)
    return tasks

# Create a task
@app.post("/tasks/", response_model=TaskRead)
async def api_create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    logger.info("POST /tasks/ endpoint called with data: %s", task.model_dump())
    return await create_task(task, db)

# Read a task by ID
@app.get("/tasks/{task_id}", response_model=TaskRead)
async def api_read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"GET /tasks/{task_id} endpoint called.")
    task = await read_task(task_id, db)
    if not task:
        logger.warning(f"Task with ID {task_id} not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update a task by ID
@app.put("/tasks/{task_id}", response_model=TaskRead)
async def api_update_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db)):
    logger.info(f"PUT /tasks/{task_id} endpoint called with data: %s", task.model_dump())
    updated_task = await update_task(task_id, task, db)
    if not updated_task:
        logger.warning(f"Task with ID {task_id} not found for update.")
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# Delete a task by ID
@app.delete("/tasks/{task_id}")
async def api_delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"DELETE /tasks/{task_id} endpoint called.")
    task = await delete_task(task_id, db)
    if not task:
        logger.warning(f"Task with ID {task_id} not found for deletion.")
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}

# Run the server with the command below
#uvicorn main:app --port 8001 --reload

