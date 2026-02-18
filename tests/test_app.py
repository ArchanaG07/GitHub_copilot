import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_and_unregister():
    # Use a test activity and email
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"

    # Sign up
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]

    # Try duplicate signup
    dup_resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert dup_resp.status_code == 400

    # Unregister
    unregister_resp = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]

    # Try unregister again
    unregister_again = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_again.status_code == 400


def test_signup_invalid_activity():
    resp = client.post("/activities/invalid_activity/signup?email=foo@bar.com")
    assert resp.status_code == 404


def test_unregister_invalid_activity():
    resp = client.post("/activities/invalid_activity/unregister?email=foo@bar.com")
    assert resp.status_code == 404
