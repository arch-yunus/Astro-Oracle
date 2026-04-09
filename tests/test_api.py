import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Celestial Intelligence Online" in response.json()["message"]

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_natal_interpret_validation():
    # Test with invalid data to check Pydantic validation
    response = client.post(
        "/api/v1/interpret/natal",
        json={"user_id": "test", "chart_data": "invalid"}
    )
    assert response.status_code == 422 # Unprocessable Entity
