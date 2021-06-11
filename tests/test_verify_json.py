from json import dumps
from typing import Callable
from flask.json import jsonify
from flask.wrappers import Response
from flask_verify.verify_json import verify_json_response
from pytest import raises


@verify_json_response
def _view_function_response() -> Response:
    """
    To test if an endpoint that already returns a response work.
        Positive test case, should work just fine.
    """
    return Response(dumps({"message": "This is a JSON."}),
                    status=200, content_type='application/json')


@verify_json_response
def _view_function_response_failure() -> Response:
    """
    To test if an endpoint that already returns a malformed response work.
        Negative test case, should raise an error that will result in a 500.
    """
    return Response("This is obviously not JSON.", content_type='plain/text',
                    status=200)



@verify_json_response
def _view_function_tuple(dictionary: dict) -> tuple[dict, int]:
    """
    To test if an endpoint that returns a tuple successfully get converted
        to a Response.
    """
    return dictionary, 200


@verify_json_response
def _view_function_tuple_failure() -> tuple[Callable, int]:
    """
    To test if an endpoint that cannot be converted into a JSON
        raises a TypeException.
    """
    return lambda x: 1, 20


@verify_json_response
def _view_function_tuple_pack() -> tuple[dict, int, int]:
    """
    To test if an endpoint that returns too many values raises
        a TypeException.
    """
    return {"msg": "This is a JSON."}, 200, 0


@verify_json_response
def _view_function_invalid_status() -> tuple[dict, str]:
    """
    To test if an endpoint that does not return a status code
        raises a TypeException.
    """
    return {"msg": "This is okay."}, "This is not a status."


def test_already_response() -> None:
    """
    Test if a view function that already returns a Response object
        does not get corrupted.
    """
    actual = _view_function_response()
    expected = Response(dumps({"message": "This is a JSON."}),
                    status=200, content_type='application/json')
    assert actual.response == expected.response
    assert actual.status_code == expected.status_code
    assert actual.content_type == expected.content_type


def test_non_json_response() -> None:
    """
    Test if a view function whose Response is not of type JSON
        successfully raises an exception.
    """
    with raises(TypeError):
        _view_function_response_failure()


def test_tuple_response() -> None:
    """
    Test if a view function that returns a tuple automatically
        gets converted to a JSON response.
    """
    dictionary = {"message": "This should be converted to JSON."}
    actual = _view_function_tuple(dictionary)
    expected = Response(dumps(dictionary), status=200, content_type='application/json')
    assert actual.content_type == expected.content_type
    assert actual.status_code == expected.status_code
    assert actual.response == expected.response


def test_tuple_response_fail() -> None:
    """
    Test the fail conditions of the view functions that return
        tuples.
    """
    fail_conditions = (_view_function_invalid_status,
                       _view_function_tuple_failure,
                       _view_function_tuple_pack)
    for fail_condition in fail_conditions:
        with raises(TypeError):
            fail_condition()
