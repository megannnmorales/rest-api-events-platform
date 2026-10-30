import jwt
from utils.config import get_secret, ALGORITHM
from utils.passwords import verify_password 
from app.models.users import get_user_by_email

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


def test_valid_create_user_request_registers_new_user(client):
    response = client.post(
        "/api/auth/register", json={"name": "Alice Smith", "email": "alice@example.com", "password": "securepassword123"}
            )
    assert response.status_code == 201
    body = response.json()
    assert body["user"]["name"] == "Alice Smith"
    
    
    
def test_password_field_not_present_in_response(client):
    response = client.post(
        "/api/auth/register", json={"name": "Alice Smith", "email": "alice@example.com", "password": "securepassword123"}
            )
    body = response.json()
    assert "hashed_password" not in body["user"]
    assert "password" not in body["user"]


def test_password_is_hashed_before_insert(client):
    client.post(
            "/api/auth/register", json={"name": "Alice Smith", "email": "alice@example.com", "password": "securepassword123"}
                )
    user = get_user_by_email("alice@example.com")

    assert user["hashed_password"] != "securepassword123"
    assert verify_password("securepassword123", user["hashed_password"])

def test_duplicate_email_responds_with_409(client):
    client.post(
                "/api/auth/register", json={"name": "Alice Smith", "email": "alice@example.com", "password": "securepassword123"}
                    ) 

    response = client.post(
                "/api/auth/register", json={"name": "Alice Smith", "email": "alice@example.com", "password": "securepassword123"}
                    ) 

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "Conflict"

def test_missing_fields_returns_400(client):
    response = client.post(
        "/api/auth/register", json={"name": "Alice Smith", "password": "securepassword123"}
            )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"