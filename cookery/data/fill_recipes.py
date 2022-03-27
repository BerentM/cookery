import requests
import json

token = input("Put jwt here: ")
url = "http://127.0.0.1:8000/recipe/new"
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

for i in range(1, 11):
    payload = json.dumps({
        "name": "Magiczne danie "+str(i),
        "difficulty": 1,
        "user_id": 1,
        "ingredients": [
            {
                "name": "string",
                "quantity": "string"
            },
            {
                "name": "string",
                "quantity": "string"
            }
        ],
        "description": [
            {
                "order": 1,
                "description": "string"
            },
            {
                "order": 2,
                "description": "string"
            }
        ]
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
