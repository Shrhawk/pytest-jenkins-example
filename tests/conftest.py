from base64 import b64encode

import pytest

from app import flask_app


@pytest.fixture(scope='session')
def app_():
    return flask_app


@pytest.fixture
def client(app_):
    """
    Flask test client
    :return:
    """
    return app_.test_client()


@pytest.fixture
def basic_auth_header():
    credentials = b64encode(b"admin:admin").decode("utf-8")
    return {"Authorization": "Basic " + credentials}
