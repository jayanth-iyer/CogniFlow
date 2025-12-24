"""
Seller router for CogniFlow.

Handles seller CRUD operations.
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.seller import Seller, SellerCreate, SellerRead, SellerStatus

router = APIRouter(prefix="/api/v1/sellers", tags=["Sellers"])


@router.post("", response_model=SellerRead, status_code=201)
def create_seller(
    seller: SellerCreate,
    session: Session = Depends(get_session)
) -> Seller:
    """Create a new seller."""
    db_seller = Seller.model_validate(seller)
    session.add(db_seller)
    session.commit()
    session.refresh(db_seller)
    return db_seller


@router.get("", response_model=list[SellerRead])
def list_sellers(
    status: Optional[SellerStatus] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
) -> list[Seller]:
    """List all sellers with optional status filter."""
    query = select(Seller)
    
    if status:
        query = query.where(Seller.status == status)
    
    query = query.offset(skip).limit(limit)
    
    return list(session.exec(query).all())


@router.get("/{seller_id}", response_model=SellerRead)
def get_seller(
    seller_id: int,
    session: Session = Depends(get_session)
) -> Seller:
    """Get a seller by ID."""
    seller = session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller


@router.patch("/{seller_id}", response_model=SellerRead)
def update_seller_status(
    seller_id: int,
    status: SellerStatus,
    session: Session = Depends(get_session)
) -> Seller:
    """Update a seller's status."""
    seller = session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    seller.status = status
    seller.updated_at = datetime.now(timezone.utc)
    session.add(seller)
    session.commit()
    session.refresh(seller)
    return seller
