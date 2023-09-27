import pytest
from fastapi.testclient import TestClient
from app.src.app import app


@pytest.fixture
def constant():
    return 5

@pytest.fixture()
def client():
    client = TestClient(app)
    return client

