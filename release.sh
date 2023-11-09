#!/bin/bash

# Build and tag container images for services

set -ex

VERSION="${1}"
DH_USER=lalanza808

# build monero-lws
cd monero-lws
HASH=$(git rev-parse HEAD)
LWS_HASH=${DH_USER}/monero-lws:${HASH}
LWS_DEV=${DH_USER}/monero-lws:develop
# bugging rn
docker build -t "${LWS_HASH}" .
docker tag "monero-lw_monero-lws:latest" "${LWS_DEV}"
docker tag "monero-lw_monero-lws:latest" "${LWS_HASH}"
docker push "${LWS_HASH}"
docker push "${LWS_DEV}"
cd ..
