import requests
import time


def test_health_endpoint_returns_healthy(base_url):
    response = requests.get(f"{base_url}/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_register_user_creates_new_user(base_url):
    payload = {"username" : f"user{time.time()}",
                    "password" : f"secure-password{time.time()}"}

    response = requests.post(f"{base_url}/api/auth/register", json=payload)

    assert response.status_code == 201
    assert payload["username"] in response.json()["user"]["username"]


def test_login_functionality(base_url, register_user_login_return_JWT):
    access_token, response = register_user_login_return_JWT

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_event_creation_with_authentications(base_url, register_user_login_return_JWT, event_payload):
    access_token, _  = register_user_login_return_JWT

    event_headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(f"{base_url}/api/events", json=event_payload, headers=event_headers)

    assert response.status_code == 201
    assert response.json()["title"] == event_payload["title"]
    assert response.json()["description"] == event_payload["description"]


def test_rsvp_to_public_event(base_url, register_user_login_return_JWT, event_payload):
    access_token, _ = register_user_login_return_JWT
    event_headers = {
        "Authorization": f"Bearer {access_token}"
    }
    new_event_response = requests.post(f"{base_url}/api/events", json=event_payload, headers=event_headers)
    event_id = new_event_response.json()["id"]
    event_body = {
        "attending": True
    }

    rsvp_response = requests.post(f"{base_url}/api/rsvps/event/{event_id}", json=event_body)

    assert rsvp_response.status_code == 201
    assert rsvp_response.json()["event_id"] == event_id


def test_400_duplicate_user_registration(base_url):
    username = f"user{time.time()}"
    password = f"secure-password{time.time()}"

    payload = {"username" : username,
               "password" : password}

    response_1 = requests.post(f"{base_url}/api/auth/register", json=payload)
    response_2 = requests.post(f"{base_url}/api/auth/register", json=payload)

    assert response_1.status_code == 201
    assert response_2.status_code == 400


def test_fail_to_create_event_without_auth(base_url, event_payload):
    new_event_response = requests.post(f"{base_url}/api/events", json=event_payload)

    assert new_event_response.status_code == 401


def test_fail_to_rsvp_private_event_without_auth(base_url, register_user_login_return_JWT, event_payload_private):
    access_token, _ = register_user_login_return_JWT
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    new_event_response = requests.post(f"{base_url}/api/events", json=event_payload_private, headers=headers)
    event_id = new_event_response.json()["id"]
    event_body = {
        "attending": True
    }
    rsvp_response = requests.post(f"{base_url}/api/rsvps/event/{event_id}", json=event_body)

    assert rsvp_response.status_code == 401




