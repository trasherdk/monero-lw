#!/bin/bash

if [[ "$(docker-compose exec -ti monero-lws monero-lws-admin list_admin)" == '{}' ]]; 
then 
    docker-compose exec -ti monero-lws monero-lws-admin create_admin;
else
    docker-compose exec -ti monero-lws monero-lws-admin list_admin;
fi