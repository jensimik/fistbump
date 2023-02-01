import pytest
from fistbump.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    with TestClient(app=app, base_url="http://test") as client:
        yield client
