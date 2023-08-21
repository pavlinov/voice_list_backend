import requests
import pytest

@pytest.fixture
def token():
    return 'mia'

@pytest.fixture
def user_id():
    return '6d687130-505c-47ff-b4c6-de0ca33de80d'

def test_get_user(token, user_id):
    url = f'http://127.0.0.1:8000/users/{user_id}?token={token}'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['id'] == user_id