FROM python:3.9-slim

ARG RETIREMENT_CALCULATOR_SERVICE_PORT

WORKDIR /app

COPY ./requirements.txt .
COPY ./retirement_calculator_service ./retirement_calculator_service

RUN pip3 install -r requirements.txt

CMD flask --app retirement_calculator_service run --host=0.0.0.0 --port=${RETIREMENT_CALCULATOR_SERVICE_PORT}