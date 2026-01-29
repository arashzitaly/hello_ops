from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_hello_with_name():
    resp = client.get("/hello", params={"name": "Ada"})
    assert resp.status_code == 200
    assert resp.json() == {"message": "hello Ada"}


def test_hello_missing_name():
    resp = client.get("/hello")
    assert resp.status_code == 422
    body = resp.json()
    assert body["detail"][0]["msg"] == "Field required"
