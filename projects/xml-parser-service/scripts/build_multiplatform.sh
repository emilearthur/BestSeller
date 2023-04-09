#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
pushd "$SCRIPT_DIR/.."
source deactivate 2>/dev/null
set -e

docker buildx create --name mybuilder --use | true

docker buildx build \
  --platform=linux/amd64,linux/arm64 \
  .. \
  -f Dockerfile \
  -t 1234455.dkr.ecr.eu-west-1.amazonaws.com/xml-parser-service:latest \
  --push

popd