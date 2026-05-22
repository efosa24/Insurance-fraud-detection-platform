from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    