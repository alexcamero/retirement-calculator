FROM python:3.9-slim

ARG USER_SERVICE_PORT

WORKDIR /app

COPY ./requirements.txt .
COPY ./user_service ./user_service

RUN pip3 install -r requirements.txt

CMD flask --app user_service run --host=0.0.0.0 --port=${USER_SERVICE_PORT}