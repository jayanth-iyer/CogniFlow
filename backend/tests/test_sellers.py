"""
Unit tests for seller endpoints.
"""

import pytest


class TestSellerEndpoints:
    """Tests for the /api/v1/sellers endpoints."""

    def test_create_seller(self, client):
        """Test creating a new seller."""
        response = client.post(
            "/api/v1/sellers",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "business_name": "Doe Enterprises"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["status"] == "pending"
        assert "id" in data

    def test_create_seller_with_phone(self, client):
        """Test creating a seller with optional phone."""
        response = client.post(
            "/api/v1/sellers",
            json={
                "name": "Jane Smith",
                "email": "jane@example.com",
                "phone": "+1234567890",
                "business_name": "Smith Co"
            }
        )
        assert response.status_code == 201
        assert response.json()["phone"] == "+1234567890"

    def test_list_sellers_empty(self, client):
        """Test listing sellers when none exist."""
        response = client.get("/api/v1/sellers")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_sellers(self, client):
        """Test listing sellers after creating some."""
        # Create two sellers
        client.post(
            "/api/v1/sellers",
            json={"name": "Seller 1", "email": "s1@test.com", "business_name": "Biz 1"}
        )
        client.post(
            "/api/v1/sellers",
            json={"name": "Seller 2", "email": "s2@test.com", "business_name": "Biz 2"}
        )

        response = client.get("/api/v1/sellers")
        assert response.status_code == 200
        sellers = response.json()
        assert len(sellers) == 2

    def test_get_seller_by_id(self, client):
        """Test getting a specific seller by ID."""
        # Create a seller
        create_response = client.post(
            "/api/v1/sellers",
            json={"name": "Test Seller", "email": "test@test.com", "business_name": "Test Biz"}
        )
        seller_id = create_response.json()["id"]

        # Get the seller
        response = client.get(f"/api/v1/sellers/{seller_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Test Seller"

    def test_get_seller_not_found(self, client):
        """Test getting a non-existent seller."""
        response = client.get("/api/v1/sellers/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Seller not found"

    def test_update_seller_status(self, client):
        """Test updating a seller's status."""
        # Create a seller
        create_response = client.post(
            "/api/v1/sellers",
            json={"name": "Status Test", "email": "status@test.com", "business_name": "Status Biz"}
        )
        seller_id = create_response.json()["id"]

        # Update status
        response = client.patch(
            f"/api/v1/sellers/{seller_id}?status=documents_submitted"
        )
        assert response.status_code == 200
        assert response.json()["status"] == "documents_submitted"

    def test_filter_sellers_by_status(self, client):
        """Test filtering sellers by status."""
        # Create sellers with different statuses
        resp1 = client.post(
            "/api/v1/sellers",
            json={"name": "Pending", "email": "p@test.com", "business_name": "P Biz"}
        )
        seller_id = resp1.json()["id"]
        
        # Update one to approved
        client.patch(f"/api/v1/sellers/{seller_id}?status=approved")

        client.post(
            "/api/v1/sellers",
            json={"name": "Pending 2", "email": "p2@test.com", "business_name": "P2 Biz"}
        )

        # Filter by approved
        response = client.get("/api/v1/sellers?status=approved")
        assert response.status_code == 200
        sellers = response.json()
        assert len(sellers) == 1
        assert sellers[0]["status"] == "approved"
