from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_documents_endpoint():

    response = client.get("/api/v1/documents/ABB")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_documents_fields():

    response = client.get("/api/v1/documents/ABB")

    row = response.json()[0]

    assert "company_id" in row
    assert "year" in row
    assert "annual_report" in row


def test_invalid_company():

    response = client.get("/api/v1/documents/XYZ123")

    assert response.status_code == 200
    assert response.json()["error"] == "Company not found"