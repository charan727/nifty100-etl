from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_get_all_companies():
    response = client.get("/api/v1/companies")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_company_has_required_fields():
    response = client.get("/api/v1/companies")

    company = response.json()[0]

    assert "id" in company
    assert "company_name" in company
    assert "website" in company
    assert "face_value" in company
    assert "book_value" in company
    assert "roce_percentage" in company
    assert "roe_percentage" in company


def test_get_company_by_id():
    response = client.get("/api/v1/companies/TCS")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "TCS"


def test_company_not_found():
    response = client.get("/api/v1/companies/XYZ123")

    assert response.status_code == 200

    data = response.json()

    assert data["error"] == "Company not found"


def test_search_company():
    response = client.get("/api/v1/search?name=tcs")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_search_invalid_company():
    response = client.get("/api/v1/search?name=abcdefghxyz")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 0