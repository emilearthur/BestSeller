#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
pushd "$SCRIPT_DIR/.."
source deactivate 2>/dev/null
set -e

ENV=${1:-dev}
VERSION_="$(git show -s --format=%cI HEAD)"
VERSION="$(sed "s/[\+\:]/-/g" <<< $VERSION_)"
COMMIT="$(git show -s --format=%h HEAD)"

source "${ENV}".env
echo "deploying to $ENV"
sam build --use-container

sam package --output-template-file .aws-sam/build/sam-template.yaml \
  --s3-bucket $BUCKET --profile $PROFILE

sam deploy --template-file .aws-sam/build/sam-template.yaml \
  --stack-name xml-parser-service-"$ENV" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides env="$ENV" Version="$VERSION" Commit="$COMMIT" \
  --capabilities CAPABILITY_NAMED_IAM \
  --profile $PROFILE