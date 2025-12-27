"""
CogniFlow Backend - FastAPI Application

AI Assistant for automating Account Manager workflows during seller onboarding.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables
from routers import sellers, documents, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler - runs on startup and shutdown."""
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="CogniFlow API",
    description="AI-powered seller onboarding assistant for Account Managers",
    version="0.2.0",
    lifespan=lifespan,
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sellers.router)
app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(auth.router)
app.include_router(dashboard.router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy"}


@app.get("/api/v1/hello", tags=["Hello"])
async def hello():
    """Simple greeting endpoint."""
    return {"message": "Hello from CogniFlow!", "version": "0.2.0"}
