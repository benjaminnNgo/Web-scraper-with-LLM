import pytest
from fastapi.testclient import TestClient

from app.main import application


@pytest.fixture
def client():
    return TestClient(application)


def test_main(client):
    response = client.get('/')
    assert response.status_code == 200
    assert len(response.text) > 0
