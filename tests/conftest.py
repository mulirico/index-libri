import pytest
from fastapi.testclient import TestClient

from index_libri.app import app


@pytest.fixture()
def client():
    return TestClient(app)
