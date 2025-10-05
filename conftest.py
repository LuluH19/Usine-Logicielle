"""
Pytest configuration and fixtures for OPS Portal tests
"""
import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app


@pytest.fixture
def app():
    """Create and configure a test instance of the app."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
        "JWT_ISSUER": "ops-portal-test",
        "JWT_AUDIENCE": "ops-test",
        "JWT_EXP_SECONDS": 3600,
    })
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers(client):
    """Get authentication headers with a valid JWT token."""
    def _get_headers(username="alice", password="alice123"):
        response = client.post(
            "/auth/login",
            json={"username": username, "password": password}
        )
        token = response.get_json()["token"]
        return {"Authorization": f"Bearer {token}"}
    
    return _get_headers
