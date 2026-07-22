import pytest
from fastapi.testclient import TestClient


@pytest.mark.usefixtures("db")
def test_health_endpoint(api_client: TestClient) -> None:
    # when
    response = api_client.get("/health")

    # then
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
