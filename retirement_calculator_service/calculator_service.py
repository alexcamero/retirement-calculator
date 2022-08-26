from datetime import date
import os, sys, json, requests
from dotenv import load_dotenv

if __name__ == "__main__":
    import users
else:
    from . import users

# HELPER FUNCTIONS

def future_value(
    present_value: float, 
    growth_rate_per_period: float, 
    number_periods: int
) -> float:
    """
    Returns the value of present_value after being compounded number_periods times at a rate of growth_rate_per_period
    """
    
    return present_value * ((1 + (growth_rate_per_period / 100)) ** number_periods)

def present_value(
    future_value: float, 
    growth_rate_per_period: float, 
    number_periods: int
) -> float:
    """
    Returns the value of future_value after discounting over number_periods periods at a rate of growth_rate_per_period. Inverse function of future_value
    """
    return future_value / ((1 + (growth_rate_per_period / 100)) ** number_periods)

def time_until_retirement(
    date_of_birth: str,
    retirement_age: int,
    current_date: str = None
) -> tuple[int, int]:
    '''
    Given date_of_birth and retirement_age, returns whole number of years from current_date (assumed to be today if omitted) until retirement and the number of days remaining after that. date_of_birth and current_date must be in 'YYYY-MM-DD' format.
    '''
    today = date.today()
    if current_date:
        try:
            today = date(*[int(s) for s in current_date.split('-')])
        except:
            # log that there was an invalid date error, and continue with current_date = today
            pass
    bday = date(*[int(s) for s in date_of_birth.split('-')])
    retirement_date = date(bday.year + retirement_age, bday.month, bday.day)
    # handle case if calculator is run after retirement
    if today >= retirement_date:
        return 0, 0
    # find date that whole number of years out that leaves less than a year remainder to retirement_date
    pre_retirement_date = date(retirement_date.year, today.month, today.day)
    if today > date(today.year, bday.month, bday.day):
        pre_retirement_date = date(retirement_date.year - 1, today.month, today.day)
    return pre_retirement_date.year - today.year, (retirement_date - pre_retirement_date).days

def age(date_of_birth: str, current_date: str = None) -> int:
    """
    Returns age of person given date_of_birth and current_date (both in 'YYYY-MM-DD' format), assuming today if current_date is left off
    """
    today = date.today()
    if current_date:
        try:
            today = date(*[int(s) for s in current_date.split('-')])
        except:
            # log that there was an invalid date error and continue with current_date = today
            pass
    bday = date(*[int(s) for s in date_of_birth.split('-')])
    bday_this_year = date(today.year, bday.month, bday.day)
    age = today.year - bday.year
    if bday_this_year > today:
        age -= 1
    return age

# MAIN FUNCTIONS

def will_have_saved(
    current_retirement_savings: float,
    household_income: float,
    current_savings_rate: float,
    date_of_birth: str,
    expected_rate_of_return: float,
    retirement_age: int,
    times_compounded_per_year: int = 1,
    income_increase_rate: float = 2,
    current_date: str = None,
    simplified: bool = True
) -> float:
    """
    Returns the total amount saved by retirement age given the current savings, future contributions, expected rate of return on investments, and date of birth. Optional parameters to change the number of times the retirment account is compounded per year, the expected rate of increase in household income, and the current date (defaults to today). Can also set the simplified parameter to False to account for actual amount of time from current_date to retirement age instead of assuming time is equal to retirement age - current age.

    date_of_birth and current_date must be in 'YYYY-MM-DD' format.

    simplifying assumptions:
      salary increases once per year beginning one year after the calculator is run
      compounding begins after the first full time period since calculator is run
      household income is received daily
      leap years do not exist
    """

    # get number of years, and leftover number of days until retirement
    # if simplified just take the time to retirement as the retirement age - current age
    if simplified:
        full_years = retirement_age - age(date_of_birth, current_date)
        remainder_days = 0
    else:
        full_years, remainder_days = time_until_retirement(date_of_birth, retirement_age, current_date)
    # calculate remaining time periods for compounding and number of days remaining after final time period
    periods_remaining = full_years * times_compounded_per_year
    additional_periods = (remainder_days * times_compounded_per_year) // 365
    periods_remaining += additional_periods
    extra_days = remainder_days - (additional_periods * (365 / times_compounded_per_year))
    # calculate prorated amount earned in the remainder days after the final time period
    base_amount = household_income * (current_savings_rate / 100)
    extra_income_at_end = (extra_days / 365) * future_value(base_amount, income_increase_rate, full_years)
    # calculate the series of payments toward retirement given the expected rate of increase for the household income 
    base_amount /= times_compounded_per_year
    payments = [current_retirement_savings] + [future_value(base_amount, income_increase_rate, i // times_compounded_per_year) for i in range(periods_remaining)]
    # return the sum of the future value of the series of payments given the expected rate of return plus the remaining prorated income
    return extra_income_at_end + sum([future_value(payments[i], expected_rate_of_return, periods_remaining - i) for i in range(len(payments))])

def need_to_have_saved(
    date_of_birth: str,
    retirement_age: int,
    life_expectancy: int,
    household_income: float,
    pre_retirement_income_percent: float,
    income_increase_rate: float = 2,
    inflation_rate: float = 3,
    expected_rate_of_return: float = 5,
    times_compounded_per_year: int = 1,
    current_date: str = None,
    simplified: bool = True
) -> float:
    """
    Returns the amount needed at the beginning of retirement to maintain the given percentage of household income in the year before retirement each year between retirement and life expectancy adjust for inflation. Uses the expected rate of return in retirement and number of times compounded per year to discount this stream of yearly income to value at the time of retirement. Can also set the simplified parameter to False to account for actual amount of time from current_date to retirement age instead of assuming time is equal to retirement age - current age.

    date_of_birth and current_date must be in 'YYYY-MM-DD' format.
    """
    # get number of whole years until retirement to calculate retirement income base amount
    # if simplified just take the time to retirement as the retirement age - current age
    if simplified:
        years_until_retirement = retirement_age - age(date_of_birth, current_date)
    else:
        years_until_retirement, _ = time_until_retirement(date_of_birth, retirement_age, current_date)
    retirement_income_base_amount = (pre_retirement_income_percent / 100) * future_value(household_income, income_increase_rate, years_until_retirement)
    # get number of retirement years
    years_of_retirement = life_expectancy - retirement_age
    # calculate retirement income needed each year adjusted for inflation
    income_needed = [future_value(retirement_income_base_amount, inflation_rate, i) for i in range(years_of_retirement)]
    # discount future yearlt income by expected rate of return in retirement
    return sum([present_value(income_needed[i], expected_rate_of_return / times_compounded_per_year, i * times_compounded_per_year) for i in range(years_of_retirement)])

def retirement_info_by_user(
    user: users.User
) -> tuple[float, float]:
    saved = will_have_saved(
        user.user_info.current_retirement_savings,
        user.user_info.household_income,
        user.user_info.current_savings_rate,
        user.user_info.date_of_birth,
        user.assumptions.expected_rate_of_return,
        user.assumptions.retirement_age
    )
    needed = need_to_have_saved(
        user.user_info.date_of_birth,
        user.assumptions.retirement_age,
        user.assumptions.life_expectancy,
        user.user_info.household_income,
        user.assumptions.pre_retirement_income_percent
    )
    return saved, needed



# quick and ugly bit here at the end to allow for just running the file from the command line given an integer argument to use to look up the user information.
if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) not in [2, 3] or (len(sys.argv) == 3 and sys.argv[2] != '--see-user'):
        print("\nIncorrect number of arguments: expecting one file name, one integer, and an optional flag '--see-user'\n")
    else:
        try:
            id = int(sys.argv[1])
            url = f"{os.getenv('USER_DATA_ENDPOINT')}{id}"
            res = requests.get(url).json()
            user = users.User(**res)
            saved, needed = retirement_info_by_user(user)
            print(f"\nTo retire at age {user.assumptions.retirement_age}:\n\nYou will need ${format(int(needed), ',d')}\n\nYou will have saved ${format(int(saved), ',d')}\n")
            if len(sys.argv) == 3:
                print(json.dumps(res), '\n')
        except:
            print("\nSomething went wrong. Make sure that you're entering an integer as an argument on the command line and that you're connected to the internet.\n")