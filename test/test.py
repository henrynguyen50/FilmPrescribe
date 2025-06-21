import requests
query = "I want something like the nice guys comedy action"
res = requests.post("http://127.0.0.1:5000/recommend", json={
    "query": query
})
print(f"{query}")
print(res.json())