docker run \
  --rm -it \
  -v $HOME/.aws/credentials:/root/.aws/credentials:ro \
  -v $PWD/xml_parser_service:/code/xml_parser_service \
  --env ENV="dev" \
  --env AWS_PROFILE="dev" \
  --env AWS_DEFAULT_REGION="eu-west-1" \
  --env EVENTS='{"Records": [{"eventVersion": "2.0", "eventSource": "aws:s3", "awsRegion": "us-east-1", "eventTime": "1970-01-01T00:00:00.000Z", "eventName": "ObjectCreated:Put", "userIdentity": {"principalId": "EXAMPLE"}, "requestParameters": {"sourceIPAddress": "127.0.0.1"}, "responseElements": {"x-amz-request-id": "EXAMPLE123456789", "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"}, "s3": {"s3SchemaVersion": "1.0", "configurationId": "testConfigRule", "bucket": {"name": "test-emile-dev", "ownerIdentity": {"principalId": "EXAMPLE"}, "arn": "arn:aws:s3:::example-bucket"}, "object": {"key": "sample.xml", "size": 1024, "eTag": "0123456789abcdef0123456789abcdef", "sequencer": "0A1B2C3D4E5F678901"}}}]}' \
  122233344.dkr.ecr.eu-west-1.amazonaws.com/xml-parser-service $@ /bin/sh