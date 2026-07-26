from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_portfolio():
    response = client.get("/api/v1/portfolio/stats")

    assert response.status_code == 200

    data = response.json()

    assert "companies" in data
    assert "avg_roe" in data
    assert "avg_roce" in data