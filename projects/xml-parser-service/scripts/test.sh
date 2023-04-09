#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
pushd "$SCRIPT_DIR/.."
source deactivate 2>/dev/null
set -e
export ENV=test
poetry run coverage run --source="./xml_parser_service" -m pytest "./tests" "$@"
poetry run coverage html
poetry run coverage report -m
popd