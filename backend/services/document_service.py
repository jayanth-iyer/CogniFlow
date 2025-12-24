"""
Document service for CogniFlow.

Handles file upload and document management operations.
"""

import os
import uuid
from typing import Optional
from fastapi import UploadFile
from sqlmodel import Session, select

from models.document import Document, DocumentCreate, DocumentStatus

UPLOAD_DIR = "uploads"


def save_uploaded_file(
    session: Session,
    file: UploadFile,
    seller_id: Optional[int] = None
) -> Document:
    """
    Save an uploaded file to disk and create a database record.
    
    Args:
        session: Database session
        file: Uploaded file from FastAPI
        seller_id: Optional seller ID to associate the document with
        
    Returns:
        Document: Created document record
    """
    # Generate unique filename to avoid collisions
    file_ext = os.path.splitext(file.filename or "file")[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Save file to disk
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    # Create database record
    document = Document(
        filename=file.filename or "unknown",
        content_type=file.content_type or "application/octet-stream",
        file_path=file_path,
        seller_id=seller_id,
        status=DocumentStatus.UPLOADED
    )
    
    session.add(document)
    session.commit()
    session.refresh(document)
    
    return document


def get_document_by_id(session: Session, document_id: int) -> Optional[Document]:
    """
    Retrieve a document by its ID.
    
    Args:
        session: Database session
        document_id: Document ID
        
    Returns:
        Document or None if not found
    """
    return session.get(Document, document_id)


def get_all_documents(
    session: Session,
    seller_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> list[Document]:
    """
    Retrieve all documents, optionally filtered by seller.
    
    Args:
        session: Database session
        seller_id: Optional seller ID to filter by
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of documents
    """
    query = select(Document)
    
    if seller_id is not None:
        query = query.where(Document.seller_id == seller_id)
    
    query = query.offset(skip).limit(limit)
    
    return list(session.exec(query).all())
