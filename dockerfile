# syntax=docker/dockerfile:1
FROM python:3.13.0b4-slim
WORKDIR /bot
RUN apt-get update && apt-get -y install make cmake opus-tools ffmpeg
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "wbot.py" ]