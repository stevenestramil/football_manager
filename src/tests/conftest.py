import pytest
from fastapi.testclient import TestClient
from main import app
from api.deps import get_storage


@pytest.fixture(autouse=True)
def reset_storage():
    get_storage.cache_clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def created_team(client):
    response = client.post("/teams", json={"name": "Arsenal", "city": "London", "titles": 13})
    return response.json()
