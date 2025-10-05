"""
Tests for health check endpoints
"""


def test_health_check(client):
    """Test /healthz endpoint"""
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.get_json()
    assert "status" in data
    assert data["status"] == "ok"


def test_readiness_check(client):
    """Test /readyz endpoint"""
    response = client.get("/readyz")
    assert response.status_code == 200
    data = response.get_json()
    assert "ready" in data
    assert data["ready"] is True


def test_root_endpoint(client):
    """Test / root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "service" in data
    assert data["service"] == "ops-portal"
    assert "version" in data
    assert "endpoints" in data
    assert "auth" in data["endpoints"]
    assert "api" in data["endpoints"]
    assert "health" in data["endpoints"]
    assert "metrics" in data["endpoints"]
