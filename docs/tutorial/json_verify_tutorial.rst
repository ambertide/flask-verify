JSON Verification
===================

One of the uses of the ``flask_verify`` package is to make sure routes correctly require JSON requests or respond
with JSON responses. This is done using simple decorators, this way, we need not worry about verifying our requests
or converting our return types in each route function.

Verifying Requests
--------------------

Imagine a function such as:

.. code-block:: python
    
    @app.route('/example_route', methods=["POST"])
    def example_view():
        if not request.json and any(key not in request.json for key in ('message', 'data')):
            return {'error': 'Not JSON'}, 400
        message = request.json['message']
        return {'message': message}, 200

Now, despite taking very small space, it is cumbersome to copy and paste the lines checking whether or not our request
contains JSON and specific keys. Furthermore, it looks confusing and hard to read at a glance. We can simplify this by
using our decorator :func:`flask_verify.verify_json.verify_json_request`, the same code snippet can be written as:

.. code-block:: python
    
    @app.route('/example_route')
    @verify_json_request(must_contain=('message', 'data'))
    def example_view():
        message = request.json['message']
        return {'message': message}, 200

Looks much simpler and much easier to read.


Verifying Responses
--------------------

Flask route functions that return compatible return types can automatically be converted without having to convert them
to JSON by hand. Normal Flask supports this with dictionaries, but ``flask_verify`` also supports\:

1. Any datatype that can be converted to a JSON string with ``dumps``. Such as ``list``.
2. Dataclass objects. Their fields and values are automatically converted into a ``dict`` and then to a JSON string.

Consider the following:

.. code-block:: python

    @dataclass
    class ExampleClass:
        a: str
        b: str

    @app.route('/example_route')
    def example_view():
        return jsonify(["hello", "world"]), 200

    @app.route('/dataclass_route')
    def dataclass_view():
        dataclass_ = ExampleClass("Hello", "world")
        return asdict(dataclass_), 200

Using :func:`flask_verify.verify_json.verify_json_response`, we can convert these two routes into a simpler form:

.. code-block:: python

    @dataclass
    class ExampleClass:
        a: str
        b: str

    @app.route('/example_route')
    @verify_json_response()
    def example_view():
        return ["hello", "world"], 200

    @app.route('/dataclass_route')
    @verify_json_response()
    def dataclass_view():
        dataclass_ = ExampleClass("Hello", "world")
        return dataclass_, 200


Combining Response and Request Verification
--------------------------------------------

In many cases, you will find yourself having Python functions that receive JSON requests and send JSON responses
at the same time, rather than writing our two decorators one after the another, you can actually combine them. For
instance, imagine a use case where we want to take a user id from the request body, then we will fetch a 
``UserInfo`` object which is a dataclass and we want to return it as JSON, this can all be done simply as:

.. code-block:: python

    @app.route('/get_info', methods=["POST"])
    @verify_json_route(must_contain=('user_id',))
    def get_user_info():
        user_info = get_user_info(request.json['user_id'])
        return user_info, 200

