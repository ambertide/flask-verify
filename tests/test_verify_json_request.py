"""
Test the verify_json_request decorator
    in flask_verify/verify_json.py
"""
from flask import Flask
from flask.testing import FlaskClient


def test_verify_json_request(client: FlaskClient) -> None:
    """
    Test if basic verify_json_request works.
    """
    resp = client.post("/without_keys", json={"Any key": "Any field."})
    assert resp.status_code == 200
    assert resp.data == b"Ok."


def test_verify_json_request_failure(client: FlaskClient) -> None:
    """
    Test if verify_json_request fails correctly.
    """
    resp = client.post("/without_keys", data=b"This is not JSON",
                       content_type="plain/text")
    assert resp.status_code == 400
    assert resp.json == {"message": "Invalid request type, not JSON."}


def test_must_contain(client: FlaskClient) -> None:
    """
    Test if request verification with must_contain works.
    """
    resp = client.post('/with_required_keys',
                       json={"message": "Required.", "data": "Required."})
    assert resp.status_code == 200
    assert resp.data == b'Ok.'  # Check if must_contain works.


def test_must_contain_fail(client: FlaskClient) -> None:
    """
    Test if must contain attribute fails correctly when a
        required key is not contained in the JSON.
    """
    resp = client.post("/with_required_keys", 
                       json={"message": "This is fine.", "but": "We miss one!"})
    assert resp.status_code == 400
    assert resp.json == {"message": "Request does not contain key data"}
