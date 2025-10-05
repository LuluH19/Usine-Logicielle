"""
Tests for authentication endpoints
"""
import pytest


def test_login_alice_ok(client):
    """Test successful login with alice user"""
    response = client.post(
        "/auth/login",
        json={"username": "alice", "password": "alice123"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
    assert len(data["token"]) > 0


def test_login_admin_ok(client):
    """Test successful login with admin user"""
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
    assert len(data["token"]) > 0


def test_login_invalid_credentials(client):
    """Test login with invalid password"""
    response = client.post(
        "/auth/login",
        json={"username": "alice", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "invalid credentials"


def test_login_missing_username(client):
    """Test login with missing username"""
    response = client.post(
        "/auth/login",
        json={"password": "alice123"}
    )
    assert response.status_code == 401


def test_login_missing_password(client):
    """Test login with missing password"""
    response = client.post(
        "/auth/login",
        json={"username": "alice"}
    )
    assert response.status_code == 401


def test_api_status_with_valid_token(client, auth_headers):
    """Test /api/status with valid token"""
    headers = auth_headers("alice", "alice123")
    response = client.get("/api/status", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert "ci" in data
    assert "artifacts" in data
    assert "monitor" in data


def test_api_status_without_token(client):
    """Test /api/status without authentication token"""
    response = client.get("/api/status")
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data


def test_api_deploy_with_alice_forbidden(client, auth_headers):
    """Test /api/deploy with alice (should be forbidden)"""
    headers = auth_headers("alice", "alice123")
    response = client.post("/api/deploy", headers=headers)
    assert response.status_code == 403
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "forbidden"


def test_api_deploy_with_admin_ok(client, auth_headers):
    """Test /api/deploy with admin (should succeed)"""
    headers = auth_headers("admin", "admin123")
    response = client.post("/api/deploy", headers=headers)
    assert response.status_code == 202
    data = response.get_json()
    assert "deployment_run_id" in data
    assert data["deployment_run_id"].startswith("run-")

