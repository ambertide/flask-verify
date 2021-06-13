from flask import Flask
from flask_verify.verify_json import verify_json_request

def create_app() -> Flask:
    app = Flask(__name__)

    @verify_json_request(must_contain=('message',))
    @app.route("/with_required_keys")
    def has_must_contain() -> tuple[str, int]:
        return "OK.", 200

    @verify_json_request()
    @app.route("/without_keys")
    def just_json() -> tuple[str, int]:
        return "Ok.", 200
