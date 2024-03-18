# For more information, please refer to https://aka.ms/vscode-docker-python
FROM nikolaik/python-nodejs:python3.12-nodejs21-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN apt-get -y update
RUN apt-get -y install git

