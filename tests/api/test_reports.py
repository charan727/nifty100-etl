from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_reports():

    r = client.get("/api/v1/reports/sectors")

    assert r.status_code == 200

    data = r.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_report_fields():

    r = client.get("/api/v1/reports/sectors")

    row = r.json()[0]

    assert "sector" in row
    assert "file" in row