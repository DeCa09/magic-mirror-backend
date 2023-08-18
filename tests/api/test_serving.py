import pytest
from fastapi.testclient import TestClient

from api.dummy import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.xfail()
def test_root_fail():
    response = client.get("/")
    assert response.json() == {"messagi": "Hello Warudo"}
