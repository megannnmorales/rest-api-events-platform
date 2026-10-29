import jwt
from utils.config import get_secret, ALGORITHM

def test_correct_username_and_password_returns_a_token(client):
    response = client.post(
        "/api/auth/login", json={
        "email": "user_c@example.com",
            "password": "password_c"
        }
    )
    body = response.json()
    
    assert response.status_code == 200
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    payload = jwt.decode(body["access_token"], get_secret(), algorithms=[ALGORITHM])
    assert payload["sub"] == "1"


def test_incorrect_email_responds_with_401(client):
    response = client.post(
        "/api/auth/login", json={
        "email": "user@example.com",
            "password": "password_c"
        }
    )
    
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "Unauthorized"


def test_incorrect_password_responds_with_401(client):
    response = client.post(
        "/api/auth/login", json={
        "email": "user_c@example.com",
            "password": "password_d"
        }
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "Unauthorized"

def test_missing_password_responds_with_400(client):
    response = client.post(
        "/api/auth/login", json={
        "email": "user_c@example.com",
        }
        )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"

def test_missing_email_responds_with_400(client):
    response = client.post(
        "/api/auth/login", json={
            "password": "password_d"
        }
        )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"