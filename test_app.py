import pytest
import json
from app import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestIndexEndpoint:
    def test_index_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_returns_json(self, client):
        response = client.get("/")
        data = json.loads(response.data)
        assert "app" in data
        assert "status" in data
        assert "environment" in data

    def test_index_status_running(self, client):
        response = client.get("/")
        data = json.loads(response.data)
        assert data["status"] == "running"


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy(self, client):
        response = client.get("/health")
        data = json.loads(response.data)
        assert data["status"] == "healthy"

    def test_health_content_type(self, client):
        response = client.get("/health")
        assert response.content_type == "application/json"


class TestErrorHandlers:
    def test_404_returns_json(self, client):
        response = client.get("/nonexistent-route")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data

    def test_404_error_message(self, client):
        response = client.get("/this/does/not/exist")
        data = json.loads(response.data)
        assert data["error"] == "Resource not found"


class TestAppConfiguration:
    def test_app_uses_env_variable(self, monkeypatch):
        monkeypatch.setenv("APP_NAME", "Test App")
        app = create_app()
        assert app.config["APP_NAME"] == "Test App"

    def test_env_variable_defaults(self):
        import os
        os.environ.pop("APP_NAME", None)
        app = create_app()
        assert app.config["APP_NAME"] == "Secure Python App"
        assert app.config["ENV"] == "production"
