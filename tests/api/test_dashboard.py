from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_dashboard():

    response = client.get("/api/v1/dashboard")

    assert response.status_code == 200

    data = response.json()

    assert "companies" in data
    assert "sectors" in data
    assert "peer_groups" in data
    assert "financial_ratios" in data