from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_get_all_sectors():
    response = client.get("/api/v1/sectors")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_sector_has_required_fields():
    response = client.get("/api/v1/sectors")
    data = response.json()

    if len(data) > 0:
        sector = data[0]
        assert "sector" in sector
        assert "company_count" in sector
        assert "avg_roe" in sector
        assert "avg_roce" in sector


def test_get_sector_companies():
    response = client.get("/api/v1/sectors/IT")
    assert response.status_code == 200


def test_invalid_sector():
    response = client.get("/api/v1/sectors/XYZ123")
    assert response.status_code == 200

    data = response.json()
    assert "error" in data