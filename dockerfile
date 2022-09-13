# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /bot
RUN apt-get update
RUN apt-get -y install make cmake opus-tools
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "wbot.py" ]