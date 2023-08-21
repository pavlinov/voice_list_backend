import pytest
import requests

@pytest.fixture
def base_url():
    return "http://127.0.0.1:8000"

def test_get_user(base_url):
    # Set up the request URL and headers
    user_id = "aeb28f5f-6d62-4533-b3bd-8b066ec0e6d4"
    token = "mia"
    url = f"{base_url}/users/{user_id}"
    headers = {"accept": "application/json"}

    # Send the GET request
    response = requests.get(url, headers=headers, params={"token": token})

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response content
    response_json = response.json()
    assert "id" in response_json
    assert "email" in response_json
    assert "username" in response_json

    # Assert the specific values returned by the API
    assert response_json["id"] == user_id
    assert response_json["email"] == "pavlinoff@hotmail.com"
    assert response_json["username"] == "pavlinov"

    # Assert other fields if needed
    assert "updated_at" in response_json
    assert "password" in response_json

    # Cleanup or additional assertions if required
