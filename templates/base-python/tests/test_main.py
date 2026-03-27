"""Tests for main application."""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_returns_welcome_message(self, client: TestClient):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome to" in data["message"]
        assert "version" in data
        assert "docs" in data


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check_returns_healthy(self, client: TestClient):
        """Test health check returns healthy status."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data


class TestReadyEndpoint:
    """Tests for readiness check endpoint."""

    def test_readiness_check_returns_ready(self, client: TestClient):
        """Test readiness check returns ready status."""
        response = client.get("/ready")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert "checks" in data
