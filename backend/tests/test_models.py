"""
Unit tests for CogniFlow models.
"""

import pytest
from datetime import datetime
from sqlmodel import Session

from models.seller import Seller, SellerStatus, SellerCreate
from models.document import Document, DocumentStatus


class TestSellerModel:
    """Tests for the Seller model."""

    def test_create_seller(self, session: Session):
        """Test creating a seller with default values."""
        seller = Seller(
            name="John Doe",
            email="john@example.com",
            business_name="Doe Enterprises"
        )
        session.add(seller)
        session.commit()
        session.refresh(seller)

        assert seller.id is not None
        assert seller.name == "John Doe"
        assert seller.email == "john@example.com"
        assert seller.business_name == "Doe Enterprises"
        assert seller.status == SellerStatus.PENDING
        assert seller.phone is None
        assert isinstance(seller.created_at, datetime)

    def test_seller_with_phone(self, session: Session):
        """Test creating a seller with phone number."""
        seller = Seller(
            name="Jane Smith",
            email="jane@example.com",
            phone="+1234567890",
            business_name="Smith Co"
        )
        session.add(seller)
        session.commit()

        assert seller.phone == "+1234567890"

    def test_seller_status_enum(self):
        """Test seller status enum values."""
        assert SellerStatus.PENDING == "pending"
        assert SellerStatus.DOCUMENTS_SUBMITTED == "documents_submitted"
        assert SellerStatus.UNDER_REVIEW == "under_review"
        assert SellerStatus.APPROVED == "approved"
        assert SellerStatus.REJECTED == "rejected"

    def test_seller_create_schema(self):
        """Test SellerCreate validation schema."""
        seller_data = SellerCreate(
            name="Test Seller",
            email="test@example.com",
            business_name="Test Business"
        )
        assert seller_data.name == "Test Seller"
        assert seller_data.email == "test@example.com"


class TestDocumentModel:
    """Tests for the Document model."""

    def test_create_document(self, session: Session):
        """Test creating a document with default values."""
        document = Document(
            filename="test.pdf",
            content_type="application/pdf",
            file_path="uploads/test.pdf"
        )
        session.add(document)
        session.commit()
        session.refresh(document)

        assert document.id is not None
        assert document.filename == "test.pdf"
        assert document.content_type == "application/pdf"
        assert document.status == DocumentStatus.UPLOADED
        assert document.seller_id is None

    def test_document_with_seller(self, session: Session):
        """Test creating a document linked to a seller."""
        # First create a seller
        seller = Seller(
            name="Test Seller",
            email="seller@example.com",
            business_name="Test Business"
        )
        session.add(seller)
        session.commit()
        session.refresh(seller)

        # Create document linked to seller
        document = Document(
            filename="invoice.pdf",
            content_type="application/pdf",
            file_path="uploads/invoice.pdf",
            seller_id=seller.id
        )
        session.add(document)
        session.commit()
        session.refresh(document)

        assert document.seller_id == seller.id

    def test_document_status_enum(self):
        """Test document status enum values."""
        assert DocumentStatus.UPLOADED == "uploaded"
        assert DocumentStatus.PROCESSING == "processing"
        assert DocumentStatus.VERIFIED == "verified"
        assert DocumentStatus.REJECTED == "rejected"
