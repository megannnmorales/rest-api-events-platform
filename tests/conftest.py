import os

os.environ["ENV"] = "test"

import pytest
from fastapi.testclient import TestClient
from db.seed_test import seed_test_data
from app.main import app
from utils.auth import create_access_token


@pytest.fixture(autouse=True)
def seed_test_db():
    seed_test_data()

@pytest.fixture
def auth_headers():
    token = create_access_token(1)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture()
def client():
    return TestClient(app)