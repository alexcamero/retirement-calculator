import requests, os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

class UserInfo:

    def __init__(
        self, 
        date_of_birth: str, 
        household_income: float, 
        current_savings_rate: float, 
        current_retirement_savings: float, 
        full_name: str, 
        address: str
    ):
        self.date_of_birth = date_of_birth
        self.household_income = float(household_income)
        self.current_savings_rate = float(current_savings_rate)
        self.current_retirement_savings = float(current_retirement_savings)
        self.full_name = full_name
        self.address = address
        # lazy validation of format of date_of_birth
        date(*[int(s) for s in self.date_of_birth.split("-")])

class UserAssumptions:

    def __init__(
        self,
        pre_retirement_income_percent: float,
        life_expectancy: int,
        expected_rate_of_return: float,
        retirement_age: int
    ):
        self.pre_retirement_income_percent = float(pre_retirement_income_percent)
        self.life_expectancy = int(life_expectancy)
        self.expected_rate_of_return = float(expected_rate_of_return)
        self.retirement_age = int(retirement_age)

class User:

    def __init__(
        self, 
        user_info: dict, 
        assumptions: dict
    ):
        self.user_info = UserInfo(**user_info)
        self.assumptions = UserAssumptions(**assumptions)

def get_user_by_id(
    id: int
) -> User:
    try:
        url = f"{os.getenv('USER_SERVICE_URL')}:{os.getenv('USER_SERVICE_PORT')}/users/{id}"
        # Attempt to get the user
        user = requests.get(url).json()
        # Attempt to cast json received as user object
        user = User(**user)
    except:
        user = None
    return user