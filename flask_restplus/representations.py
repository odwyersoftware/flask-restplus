# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

try:
    from ujson import dumps
except ImportError:
    from json import dumps

from marshmallow.schema import Schema

from flask import make_response, current_app


def output_json(data, code, headers=None):
    '''Makes a Flask response with a JSON encoded body'''

    settings = current_app.config.get('RESTPLUS_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.
    if current_app.debug:
        settings.setdefault('indent', 4)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262

    # Fix for object is not serializable error.
    if (
        isinstance(data, dict) and
        'schema' in data and
        isinstance(data['schema'], Schema)
    ):
        data.pop('schema', None)
    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
