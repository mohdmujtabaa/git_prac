from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL (update this based on your database)
DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"

# Async database engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Session factory
async_session_factory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()