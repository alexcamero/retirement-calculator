from user_service import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_endpoint(user_client):
    response = user_client.get('/users/55')
    assert response.status_code == 200
    assert response.get_json() == {
        "user_info": {
            "date_of_birth": "2001-04-21",
            "household_income": 170392,
            "current_savings_rate": 18,
            "current_retirement_savings": 458215,
            "full_name": "Shane Moore",
            "address": "USNV Goodwin\nFPO AA 94241"
        },
        "assumptions": {
            "pre_retirement_income_percent": 73,
            "life_expectancy": 79,
            "expected_rate_of_return": 8,
            "retirement_age": 67
        }
    }