"""
Document model for CogniFlow.

Represents documents uploaded during seller onboarding.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field


def utc_now() -> datetime:
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(timezone.utc)


class DocumentStatus(str, Enum):
    """Status of document processing."""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    VERIFIED = "verified"
    REJECTED = "rejected"


class DocumentBase(SQLModel):
    """Base document model with common fields."""
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(max_length=100)


class Document(DocumentBase, table=True):
    """Document database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    seller_id: Optional[int] = Field(default=None, foreign_key="seller.id")
    file_path: str = Field(max_length=500)
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED)
    created_at: datetime = Field(default_factory=utc_now)


class DocumentCreate(SQLModel):
    """Schema for document creation (internal use)."""
    filename: str
    content_type: str
    file_path: str
    seller_id: Optional[int] = None


class DocumentRead(DocumentBase):
    """Schema for reading document data."""
    id: int
    seller_id: Optional[int]
    file_path: str
    status: DocumentStatus
    created_at: datetime
