import requests

email_data = {
    "email": "john.doe@example.com"
}

response = requests.post("http://127.0.0.1:5000/login", json=email_data)

if response.status_code == 200:
    api_key = response.json().get("api_key")
    print(f"API key: {api_key}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())

