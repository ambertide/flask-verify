# flask-verify

[![Python package](https://github.com/ambertide/flask-verify/actions/workflows/python-package.yml/badge.svg)](https://github.com/ambertide/flask-verify/actions/workflows/python-package.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/d052e70921b90955244f/maintainability)](https://codeclimate.com/github/ambertide/flask-verify/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d052e70921b90955244f/test_coverage)](https://codeclimate.com/github/ambertide/flask-verify/test_coverage)
[![Documentation Status](https://readthedocs.org/projects/flask-verify/badge/?version=latest)](https://flask-verify.readthedocs.io/en/latest/?badge=latest)

A python package to verify the content of Requests and convert the return values of view functions in Flask applications.



## Installation

You can install `flask-verify`

```bash
pip install flask-verify
```


## Example

Consider this minimal example, where `Message` is a simple dataclass.

```python
from flask_verify.verify_json import verify_json_route
from flask import Flask, request

app = Flask(__name__)

@app.route('/example', methods=['POST'])
@verify_json_route(must_contain=('message', 'username'))
def example_route():
    message = Message(request.json['username'], request.json['message'])
    return message, 200
```

Just by writing a single decorator statement, we have:

1. Ensured that the `Request` is of type `application/json` and contains keys `message` and `username`, if this is not true, our server will respond with a 400 status code Response explaining the issue to the server, including the name of the first missing key if that exists.
2. Converted the return type to JSON, `message` object is an instance of the `Message` dataclass, thanks to our decorator, the Response will automatically be converted to a JSON containing the field names and values of the dataclass instance.

[Read the Docs](https://flask-verify.readthedocs.io/en/latest/index.html)
