"""
Pytest configuration and fixtures for CogniFlow tests.
"""

import os
import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient

# Import models so they register with SQLModel.metadata
from models.seller import Seller  # noqa: F401
from models.document import Document  # noqa: F401

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(name="engine", scope="function")
def engine_fixture():
    """Create a test database engine."""
    # Remove test database if exists
    if os.path.exists("./test.db"):
        os.remove("./test.db")
    
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    
    # Cleanup
    SQLModel.metadata.drop_all(engine)
    engine.dispose()
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create a test database session."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(engine):
    """Create a test client with overridden database dependency."""
    # Override database module before importing app
    import database
    original_engine = database.engine
    database.engine = engine
    
    # Import app after overriding engine
    from main import app
    
    def get_test_session():
        with Session(engine) as session:
            yield session
    
    app.dependency_overrides[database.get_session] = get_test_session
    
    with TestClient(app, raise_server_exceptions=True) as client:
        yield client
    
    app.dependency_overrides.clear()
    database.engine = original_engine


@pytest.fixture
def upload_dir(tmp_path):
    """Create a temporary upload directory."""
    upload_path = tmp_path / "uploads"
    upload_path.mkdir()
    
    # Override the upload directory
    original_dir = os.environ.get("UPLOAD_DIR")
    os.environ["UPLOAD_DIR"] = str(upload_path)
    
    yield upload_path
    
    # Restore original
    if original_dir:
        os.environ["UPLOAD_DIR"] = original_dir
    else:
        os.environ.pop("UPLOAD_DIR", None)
