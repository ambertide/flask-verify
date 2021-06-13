"""
Functions in this module are checked to verify
that either the request or the response of a Flask
route Function is a JSON.
"""
from functools import wraps
from typing import Any, Callable, Iterable, Union, Optional
from flask import Response, request
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
    @wraps(route)
    def wrapper(*args, **kwargs) -> Response:
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
        except (ValueError, AssertionError, TypeError) as exception:
            raise TypeError("Invalid view function return type.") from exception
    return wrapper


def verify_json_request(must_contain: Optional[Iterable] = None) -> Callable:
    """
    Verify that a request sent to a Flask route has a request
        of MIME type Application/JSON.

    :param must_contain: If provided, JSON collection is checked
        if it contains items provided.
    :return A view route that checks JSON requirements before executing
        requests.
    """
    if must_contain is None:
        must_contain = []
    def verify_json_request_wrapper(route: Callable) -> Callable:
        """
        Wrapper function around the decorator.
        """
        @wraps(route)
        def wrapper(*args, **kwargs) -> Any:
            if (json := request.json) is None:  # If Request is not of application/json type.
                return Response(dumps({"message": "Invalid request type, not JSON."}),
                                     status=400, content_type="application/json")
            if any((k:=key) not in json for key in must_contain):
                # If one of the keys is not in the JSON request body.
                return Response(dumps({"message": f"Request does not contain key {k}"}),
                                  status=400, content_type="application/json")
            return route(*args, **kwargs)  # Otherwise everything is fine.
        return wrapper
    return verify_json_request_wrapper
