#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
pushd "$SCRIPT_DIR/.."
source deactivate 2>/dev/null
set -e
export ENV=test
export PYTHONPATH="./src"
coverage run --source="./src/xml_parser_service" -m pytest "./tests" "$@"
coverage html
coverage report -m
popd