from api.dummy import app

from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.xfail()
def test_root_fail():
    response = client.get("/")
    assert response.json() == {"messagi": "Hello Warudo"}
