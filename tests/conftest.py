import pytest
from user_service import create_app as create_user_app
from retirement_calculator_service import create_app as create_calculator_app

@pytest.fixture
def user_app():
    app = create_user_app({'TESTING': True})
    return app

@pytest.fixture
def calculator_app():
    app = create_calculator_app({'TESTING': True})
    return app

@pytest.fixture
def user_client(user_app):
    return user_app.test_client()

@pytest.fixture
def calculator_client(calculator_app):
    return calculator_app.test_client()