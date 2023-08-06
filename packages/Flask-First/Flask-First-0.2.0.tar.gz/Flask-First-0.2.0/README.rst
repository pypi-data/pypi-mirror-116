Flask-First
===========


Flask extension for using "specification first" principle.

Features:

* Decorator for mapping routes from OpenAPI specification on Python's view functions via Flask.
* Validating path parameters from url.
* Validating arguments from url.
* Validating JSON from request.
* Validating response.

----

Limitations

* All specification in one file.
* Not supported request headers.
* Not supported xml.
* Not supported ``External Documentation Object``.
* Not supported ``allOf``, ``oneOf``, ``anyOf``.
* Not supported ``Encoding Object``.
* Not supported ``Callback Object``.
* Not supported ``Example Object``.
* Not supported ``Link Object``.
* Not supported ``Discriminator Object``.
* Not supported ``XML Object``.
* Not supported ``Specification Extensions``.
* Not supported ``OAuthFlowsObject``.


----

.. contents:: Contents


Installing
----------

Install and update using `pip`_:

.. code-block:: text

  $ pip install flask_first

.. _pip: https://pip.pypa.io/en/stable/quickstart/

Simple example
--------------
OpenAPI 3 specification file ``openapi.yaml``:

.. code-block:: yaml

    openapi: 3.0.3
    info:
      title: Simple API for Flask-First
      version: 1.0.0
    paths:
      /{name}:
        parameters:
          - name: name
            in: path
            required: true
            schema:
              type: string
        get:
          operationId: index
          summary: Returns a list of items
          responses:
            '200':
              description: OK

File with application initialization ``main.py``:

.. code-block:: python

    import os

    from flask import Flask
    from flask_first import First

    basedir = os.path.abspath(os.path.dirname(__file__))
    path_to_spec = os.path.join(basedir, 'openapi.yaml')

    app = Flask(__name__)
    app.config['FIRST_RESPONSE_VALIDATION'] = True
    First(app, path_to_spec=path_to_spec)


    @app.specification
    def index(name):
        return f'Hello, {name}!'

    if __name__ == '__main__':
        app.run()

Run application:

.. code-block:: text

  $ python main.py

Check url in browser ``http://127.0.0.1:5000/username``.

Settings
--------

**FIRST_RESPONSE_VALIDATION**
    Default: `False`.

    Enabling response body validation. Useful when developing. May be disabled in a production environment.

Additional documentation
------------------------

* `OpenAPI Documentation <https://swagger.io/specification/>`_
* `JSON Schema Documentation <https://json-schema.org/specification.html>`_
