"""
Chat router for CogniFlow.

Handles chat interactions with the AI agent.
"""

from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from agents.onboarding_agent import invoke_agent

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str
    seller_id: Optional[int] = None
    history: Optional[list[dict]] = None


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    response: str
    messages: list[dict]
    current_step: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a message to the onboarding agent.
    
    The agent uses Ollama with Llama 3.2 to provide helpful responses
    about the seller onboarding process.
    """
    result = invoke_agent(
        message=request.message,
        seller_id=request.seller_id,
        history=request.history
    )
    
    return ChatResponse(
        response=result["response"],
        messages=result["messages"],
        current_step=result["current_step"]
    )
