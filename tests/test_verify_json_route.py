"""
Used to test the verify_json_route decorator.
"""
from flask.testing import FlaskClient


def test_verify_json_route_s(client: FlaskClient) -> None:
    """
    Let us test if the verify_json_route works successfully.
    """
    resp = client.post('/requires_and_responds_json', json={"message": "Hello"})
    assert resp.status_code == 200
    assert resp.json == {"echo": "Hello"}


def test_verify_json_route_failure(client: FlaskClient) -> None:
    """
    Test if verify_json_route fails correctly upon non-JSON request..
    """
    resp = client.post("/requires_and_responds_json", data=b"This is not JSON",
                       content_type="plain/text")
    assert resp.status_code == 400
    assert resp.json == {"message": "Invalid request type, not JSON."}


def test_must_contain_route_fail(client: FlaskClient) -> None:
    """
    Test if must contain attribute fails correctly when a
        required key is not contained in the JSON.
    """
    resp = client.post("/requires_and_responds_json", 
                       json={"but": "We miss one!"})
    assert resp.status_code == 400
    assert resp.json == {"message": "Request does not contain key message"}