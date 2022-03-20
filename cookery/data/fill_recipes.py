import requests
import json

url = "http://127.0.0.1:8000/recipe/new"
headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzcyIsImV4cCI6MTY0Nzc5NDE2Mn0.MjHyAhjwNtFW_X9UD-sNkfijsXimpKB5gFhGznz540A',
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


