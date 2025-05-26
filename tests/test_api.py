from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_task():
    response = client.get("/api/task")
    assert response.status_code == 200
    assert "task" in response.json()

def test_submit_response():
    response = client.post("/api/response", json={"task_id": 1, "response": "sample response"})
    assert response.status_code == 201
    assert response.json() == {"message": "Response recorded successfully."}

def test_get_results():
    response = client.get("/api/results")
    assert response.status_code == 200
    assert "results" in response.json()