FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y python3 python3-venv
WORKDIR /srv/lws-web
COPY . .
RUN python3 -m venv .venv
RUN .venv/bin/pip install poetry
RUN .venv/bin/poetry install
