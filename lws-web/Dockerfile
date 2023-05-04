FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y python3 python3-venv
WORKDIR /srv/lws-web
RUN adduser \
   --system \
   --shell /bin/bash \
   --gecos 'lws-web' \
   --group \
   --disabled-password \
   --home /srv/lws-web \
   --uid 1000 \
   lws-web
COPY . .
RUN chown -R lws-web:lws-web .
RUN python3 -m venv .venv
RUN .venv/bin/pip install poetry
RUN .venv/bin/poetry install

CMD ".venv/bin/poetry run start"