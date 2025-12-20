import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app


@pytest.fixture
def client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    return flask_app.test_client()