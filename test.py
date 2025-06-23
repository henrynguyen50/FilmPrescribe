from fastapi.testclient import TestClient
from backend.app import app #have to import app instance for fastapi

client = TestClient(app)

query = "I want batman"

def test_recommend():
    response = client.post("http://127.0.0.1:8000/recommend", json={"query": query})
    print(f"{query}")
    print(response.json())

test_recommend()
