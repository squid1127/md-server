"""Test script: Create document with default content."""

import requests

API_URL = "http://localhost:8000/api/new"
API_KEY = "3474df16639a411404859acc549fad70a28a20fc273921a7"

TITLE = "Test Document"
CONTENT = "# This is a test document\n\nThis document was created via the API."

response = requests.post(
    API_URL,
    json={
        "title": TITLE,
        "content": CONTENT,
    },
    headers={"X-API-KEY": API_KEY},
)

if response.status_code == 200:
    print("Document created successfully:")
    print(response.json())
else:
    print("Error creating document:")
    print(response.json())
