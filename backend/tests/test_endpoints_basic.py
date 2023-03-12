import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    ["url", "expected_status_code"],
    (
        ("/strip", 200),
        ("/calendar", 200),
        # ("/hours", 200),
        # ("/popular_hours", 200),
        ("/some_random_url", 404),
    ),
)
def test_endpoint_generic(url, expected_status_code, client: TestClient):
    response = client.get(url)
    assert response.status_code == expected_status_code
