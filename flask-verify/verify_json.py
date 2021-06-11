"""
Functions in this module are checked to verify
that either the request or the response of a Flask
route Function is a JSON.
"""
from functools import wraps
from typing import Any, Callable, Union
from flask import Response
from json import dumps


JSONSerializable = Union[dict[str, Any], list[Any]]
JSONRoute = Union[Callable[..., tuple[JSONSerializable, int]],
                  Callable[..., Response]]


def verify_json_response(route: JSONRoute) -> Callable[..., Response]:
    """
    Verify that a Flask route returns a JSON Response,
        effectively by converting Flask routes to return
        Responses with JSON.

    :param route: A route view function that either returns
    a Response itself or a tuple[JSONSerializable, int] where
    its first value is the response body and second value is
    the status code.
    :return Is a route function that either returns the same
    Response as the original route function if it returned a
    Response or a Response whose status code and body is taken
    from the tuple that is the return type of the original
    view function.
    """
    @wraps
    def route_returns_json(*args, **kwargs) -> Response:
        response = route(*args, **kwargs)  # Get the response first.
        if isinstance(response, Response):
            if response.content_type == 'application/json':
                return response  # Already of the right type.
            raise TypeError("Invalid response mimetype.")
        try:
            body, status_code = response
            assert isinstance(status_code, int)
            response = Response(dumps(body), status=status_code,
                                content_type="application/json")
            return response
        except (ValueError, AssertionError, TypeError):
            raise TypeError("Invalid view function return type.")
    return route_returns_json
