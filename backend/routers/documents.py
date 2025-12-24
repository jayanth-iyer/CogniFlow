"""
Document router for CogniFlow.

Handles document upload and retrieval.
"""

from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session

from database import get_session
from models.document import DocumentRead
from services import document_service

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])

# Allowed file types for upload
ALLOWED_CONTENT_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/gif",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]


@router.post("/upload", response_model=DocumentRead, status_code=201)
def upload_document(
    file: UploadFile = File(...),
    seller_id: Optional[int] = None,
    session: Session = Depends(get_session)
) -> DocumentRead:
    """
    Upload a document.
    
    Accepts PDF, images (JPEG, PNG, GIF), and Word documents.
    Optionally associates the document with a seller.
    """
    # Validate file type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file.content_type}' not allowed. Allowed types: {ALLOWED_CONTENT_TYPES}"
        )
    
    document = document_service.save_uploaded_file(
        session=session,
        file=file,
        seller_id=seller_id
    )
    
    return document


@router.get("", response_model=list[DocumentRead])
def list_documents(
    seller_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
) -> list[DocumentRead]:
    """List all documents with optional seller filter."""
    return document_service.get_all_documents(
        session=session,
        seller_id=seller_id,
        skip=skip,
        limit=limit
    )


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(
    document_id: int,
    session: Session = Depends(get_session)
) -> DocumentRead:
    """Get a document by ID."""
    document = document_service.get_document_by_id(session, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
