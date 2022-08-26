# retirement-calculator

Here are a few options for running the project.

## Run API via docker-compose

1. Install docker
2. Set `USER_SERVICE_URL=http://user_service` in the `.env` file
3. run `docker compose up --build` (or `docker-compose up --build`) from the command line in the project's root directory

## Run API without docker

1. Install some recent version of python (I used 3.9, but I don't imagine there will be a difference as long as you keep it above 3.6 or so)
2. Set up a python virtual environment in the root directory of the project by running `python3 -m venv venv` and source with either `source venv/bin/activate` for mac/unix or `venv\Scripts\activate.bat` for windows (go to https://docs.python.org/3/tutorial/venv.html for more help)
3. Run `pip3 install -r requirements.txt`
4. Make sure `USER_SERVICE_URL=http://localhost` (or whatever your local host is) in the `.env` file
5. Run 
```
flask --app user_service run --port=5002 & flask --app retirement_calculator_service run --port=5001
```
(or whatever ports you want to use, just make sure they match what is in the `.env` file)

## API

Assuming one of the two methods above was successful, you should be able to hit the endpoints from `localhost` or `127.0.0.1` or whatever address your computer typically uses for local hosting.

The user service (running on port 5002 or whatever you set) has just one endpoint at `/users/{id}` that takes GET requests and responds with the user data for the given `id`. So sending a GET request to `http://127.0.0.1:5002/users/55` should return the same thing as `https://pgf7hywzb5.execute-api.us-east-1.amazonaws.com/users/55`. So the service is a pointless fiction here, but I wanted to give an example of how I would build a larger system out by making it its own thing to run.

The retirement calculator service (running on port 5001 or whatever you set) has an endpoint `/retirement_calculator` that takes a POST request of a json object of the same form as the payload described in the prompt, eg
```
{
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
```
It should return a json response with the total amount that will be saved by retirement and the amount that should be saved by retirement, both as unrounded floats, eg
```
{
	"saved": 32147772.05082413,
	"needed": 3346427.4147260543
}
```

Alternatively, you can send a GET request to the endpoint `/retirement_calculator/{id}` to retrieve the same kind of response for the user corresponding to the provided `id`. The service will then make a call to the user service for the user's information.

## Run single file script from command line

If you don't want to run the whole API you can just run the script `./retirement_calculator_service/calculator_service.py` from the command line along with an integer argument for the user id. Run
```
python3 ./retirement_calculator_service/calculator_service.py 55
```
to have the results printed to the console (with rounding!). You can also run
```
python3 ./retirement_calculator_service/calculator_service.py 55 --see-user
```
where the optional see-user flag will print out the user details as well.

## Testing

As long as everything went well with setting up the python environement, testing should work just by running the `pytest` command from the root directory.

## To-do

- Error-handling and logging didn't get enough attention. In particular, things might behave poorly if dates are out of their typical "birthday < today < retirement day < death day" order or if negative numbers are introduced in unexpected places. Of course, some of these things might be ok like "today < birthday" if some parent-to-be is ahead of the game, but didn't have a chance to sit down and take care of all possibilities.
- Along the same lines, there obviously need to be more unit tests. This was just an issue of time on my end.
- In terms of the calculator service itself, it could be made more flexible to handle different situations. I did add some optional parameters to change the current date, change the number of times the investments comound in a year, and get more specific about the time left before retirement. But more could be done so that individual users could customize it to their particular situation.
- I was going to try to do something slick with `config.py` files so that the user_service url wouldn't need to be changed if you're running it on docker or just running it open for debugging, but I didn't get to it.
