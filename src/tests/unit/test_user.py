from starlette.testclient import TestClient


def test_success_login(
    client: TestClient,
    login_path: str,
    valid_user_credentials: dict,
):
    response = client.post(
        url=login_path,
        json=valid_user_credentials,
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_failed_login(
    client: TestClient,
    login_path: str,
    invalid_user_credentials: dict,
):
    response = client.post(
        url=login_path,
        json=invalid_user_credentials,
    )
    assert response.status_code == 400
