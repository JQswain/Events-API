import pytest
import requests
import time

@pytest.fixture
def base_url():
    return  "http://127.0.0.1:5000"

@pytest.fixture
def register_user_login_return_JWT(base_url):
    username = f"user{time.time()}"
    password = f"secure-password{time.time()}"

    payload = {"username" : username,
           "password" : password }

    requests.post(f"{base_url}/api/auth/register", json=payload)

    login_response = requests.post(f"{base_url}/api/auth/login", json=payload)
    access_token = login_response.json()["access_token"]
    print(access_token)

    return access_token, login_response

@pytest.fixture
def event_payload():
    timestamp = int(time.time())

    return {
        "title": f"Meeting-{timestamp}",
        "description": f"Meeting about topic-{timestamp}",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

@pytest.fixture
def login(base_url):
    payload = {
        "username": "josh_swain",
        "password": "BetstPassword123"
    }

    response = requests.post(f"{base_url}/api/auth/login", json=payload)
    data = response.json()
    access_token = data["access_token"]

    return access_token

@pytest.fixture
def event_payload_private():
    timestamp = int(time.time())

    return {
        "title": f"Meeting-{timestamp}",
        "description": f"Meeting about topic-{timestamp}",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": False,
        "requires_admin": False
    }