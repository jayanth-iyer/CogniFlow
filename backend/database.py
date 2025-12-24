"""
Database configuration for CogniFlow.

Uses SQLModel with SQLite for local development.
"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# SQLite database URL - stores in backend directory
DATABASE_URL = "sqlite:///./cogniflow.db"

# Create engine with SQLite-specific settings
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
)


def create_db_and_tables() -> None:
    """Create all database tables from SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    
    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session
