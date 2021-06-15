from flask import Flask, request
from flask.testing import FlaskClient
from flask_verify.verify_json import verify_json_request, verify_json_route
import pytest


def create_app() -> Flask:
    """
    Create an app for testing.
    """
    app = Flask(__name__)

    @app.route("/with_required_keys", methods=["POST"])
    @verify_json_request(must_contain=('message', 'data'))
    def has_must_contain() -> tuple[str, int]:
        return "Ok.", 200

    @app.route("/without_keys", methods=["POST"])
    @verify_json_request()
    def just_json() -> tuple[str, int]:
        return "Ok.", 200

    @app.route("/requires_and_responds_json", methods=["POST"])
    @verify_json_route(must_contain=('message',))
    def full_json() -> tuple[str, int]:
        return {'echo': request.json['message']}, 200

    return app


@pytest.fixture
def client() -> FlaskClient:
    """
    Fixture used to run API tests.
    """
    app = create_app()
    with app.test_client() as client_:
        yield client_
