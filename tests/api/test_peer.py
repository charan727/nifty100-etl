from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_get_peer_groups():

    response = client.get("/api/v1/peer-groups")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_peer_group_fields():

    response = client.get("/api/v1/peer-groups")

    data = response.json()

    if len(data) > 0:

        row = data[0]

        assert "peer_group_name" in row
        assert "company_count" in row


def test_peer_group_companies():

    response = client.get("/api/v1/peer-groups/Private Banks")

    assert response.status_code == 200


def test_invalid_peer_group():

    response = client.get("/api/v1/peer-groups/XYZ123")

    assert response.status_code == 200

    assert "error" in response.json()