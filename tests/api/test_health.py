from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_health_status():
    response = client.get("/api/v1/health")
    data = response.json()
    assert data["status"] == "ok"


def test_health_version():
    response = client.get("/api/v1/health")
    data = response.json()
    assert "version" in data





def test_health_db_counts():
    response = client.get("/api/v1/health")
    data = response.json()
    assert "db_row_counts" in data
    assert isinstance(data["db_row_counts"], dict)


def test_health_content_type():
    response = client.get("/api/v1/health")
    assert response.headers["content-type"].startswith("application/json")