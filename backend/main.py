"""
CogniFlow Backend - FastAPI Application

AI Assistant for automating Account Manager workflows during seller onboarding.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CogniFlow API",
    description="AI-powered seller onboarding assistant for Account Managers",
    version="0.1.0",
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy"}


@app.get("/api/v1/hello", tags=["Hello"])
async def hello():
    """Simple greeting endpoint."""
    return {"message": "Hello from CogniFlow!", "version": "0.1.0"}
