from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_screener_endpoint():

    response = client.get("/api/v1/screener")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_screener_filter():

    response = client.get(
        "/api/v1/screener?min_roe=10&min_roce=10"
    )

    assert response.status_code == 200


def test_screener_fields():

    response = client.get("/api/v1/screener")

    data = response.json()

    if len(data) > 0:

        company = data[0]

        assert "id" in company
        assert "company_name" in company
        assert "roe_percentage" in company
        assert "roce_percentage" in company
        assert "book_value" in company
        assert "face_value" in company