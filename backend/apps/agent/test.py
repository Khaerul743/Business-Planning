import requests
response = requests.post(f"http://localhost:8000/api/document_knowladge/similarity_search", json={"agent_id": "a04b8eb2-3b32-44e2-9a6a-bbca2c23ab58", "query": "Paradigma arsitektur langgraph"})
if response.status_code != 200:
    print("Terjadi kesalahan sistem saat mendapatkan dokument knowledge")
result = response.json()
print(result["data"]["result"])