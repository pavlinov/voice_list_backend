import pytest
import requests

@pytest.fixture
def url():
    return "http://127.0.0.1:8000/users?token=mia"

def test_create_user(url):
    headers = {
        'accept': 'application/json',
        'x-token': 'fake-super-secret-token'
    }
    data = {
        "password": "temp1234",
        "username": "apavlinov",
        "email": "apavlinov@example.com"
    }
    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 200
    assert response.json()['ResponseMetadata']['HTTPStatusCode'] == 200