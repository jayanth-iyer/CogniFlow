"""
Seller model for CogniFlow.

Represents sellers being onboarded to the e-commerce platform.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field


def utc_now() -> datetime:
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(timezone.utc)


class SellerStatus(str, Enum):
    """Status of the seller onboarding process."""
    PENDING = "pending"
    DOCUMENTS_SUBMITTED = "documents_submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class SellerBase(SQLModel):
    """Base seller model with common fields."""
    name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=5, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    business_name: str = Field(min_length=1, max_length=255)


class Seller(SellerBase, table=True):
    """Seller database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    status: SellerStatus = Field(default=SellerStatus.PENDING)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class SellerCreate(SellerBase):
    """Schema for creating a new seller."""
    pass


class SellerRead(SellerBase):
    """Schema for reading seller data."""
    id: int
    status: SellerStatus
    created_at: datetime
    updated_at: datetime
