from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_tearsheet():

    r = client.get("/api/v1/tearsheet/Tata")

    assert r.status_code == 200

    data = r.json()

    assert "company" in data
    assert "file" in data


def test_invalid_company():

    r = client.get("/api/v1/tearsheet/XYZ123")

    assert r.status_code == 200
    assert r.json()["error"] == "Tearsheet not found"