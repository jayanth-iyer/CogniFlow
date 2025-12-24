"""
Unit tests for document endpoints.
"""

import io
import pytest


class TestDocumentEndpoints:
    """Tests for the /api/v1/documents endpoints."""

    def test_upload_document(self, client):
        """Test uploading a document."""
        # Create a fake PDF file
        file_content = b"%PDF-1.4 fake pdf content"
        files = {
            "file": ("test.pdf", io.BytesIO(file_content), "application/pdf")
        }

        response = client.post("/api/v1/documents/upload", files=files)
        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == "test.pdf"
        assert data["content_type"] == "application/pdf"
        assert data["status"] == "uploaded"
        assert "id" in data

    def test_upload_document_with_seller(self, client):
        """Test uploading a document linked to a seller."""
        # First create a seller
        seller_response = client.post(
            "/api/v1/sellers",
            json={"name": "Doc Seller", "email": "doc@test.com", "business_name": "Doc Biz"}
        )
        seller_id = seller_response.json()["id"]

        # Upload document with seller_id
        file_content = b"%PDF-1.4 seller document"
        files = {"file": ("seller_doc.pdf", io.BytesIO(file_content), "application/pdf")}

        response = client.post(
            f"/api/v1/documents/upload?seller_id={seller_id}",
            files=files
        )
        assert response.status_code == 201
        assert response.json()["seller_id"] == seller_id

    def test_upload_invalid_file_type(self, client):
        """Test uploading a file with invalid content type."""
        file_content = b"not a valid file"
        files = {
            "file": ("test.exe", io.BytesIO(file_content), "application/x-msdownload")
        }

        response = client.post("/api/v1/documents/upload", files=files)
        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"]

    def test_upload_image(self, client):
        """Test uploading an image file."""
        # Minimal JPEG header
        file_content = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01'
        files = {
            "file": ("photo.jpg", io.BytesIO(file_content), "image/jpeg")
        }

        response = client.post("/api/v1/documents/upload", files=files)
        assert response.status_code == 201
        assert response.json()["content_type"] == "image/jpeg"

    def test_list_documents_empty(self, client):
        """Test listing documents when none exist."""
        response = client.get("/api/v1/documents")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_documents(self, client):
        """Test listing documents after uploading some."""
        # Upload two documents
        for i in range(2):
            files = {
                "file": (f"doc{i}.pdf", io.BytesIO(b"%PDF-1.4"), "application/pdf")
            }
            client.post("/api/v1/documents/upload", files=files)

        response = client.get("/api/v1/documents")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_document_by_id(self, client):
        """Test getting a specific document by ID."""
        # Upload a document
        files = {"file": ("get_test.pdf", io.BytesIO(b"%PDF-1.4"), "application/pdf")}
        upload_response = client.post("/api/v1/documents/upload", files=files)
        doc_id = upload_response.json()["id"]

        # Get the document
        response = client.get(f"/api/v1/documents/{doc_id}")
        assert response.status_code == 200
        assert response.json()["filename"] == "get_test.pdf"

    def test_get_document_not_found(self, client):
        """Test getting a non-existent document."""
        response = client.get("/api/v1/documents/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Document not found"

    def test_filter_documents_by_seller(self, client):
        """Test filtering documents by seller_id."""
        # Create a seller
        seller_response = client.post(
            "/api/v1/sellers",
            json={"name": "Filter Seller", "email": "filter@test.com", "business_name": "Filter Biz"}
        )
        seller_id = seller_response.json()["id"]

        # Upload document for this seller
        files = {"file": ("seller_doc.pdf", io.BytesIO(b"%PDF-1.4"), "application/pdf")}
        client.post(f"/api/v1/documents/upload?seller_id={seller_id}", files=files)

        # Upload document without seller
        files = {"file": ("no_seller.pdf", io.BytesIO(b"%PDF-1.4"), "application/pdf")}
        client.post("/api/v1/documents/upload", files=files)

        # Filter by seller
        response = client.get(f"/api/v1/documents?seller_id={seller_id}")
        assert response.status_code == 200
        docs = response.json()
        assert len(docs) == 1
        assert docs[0]["seller_id"] == seller_id
