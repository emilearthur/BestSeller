# XML Parser Service

Ensure the following application are installed before running anything in the repository.

* [Docker](https://www.docker.com/)
* [Docker buildx](https://docs.docker.com/build/install-buildx/)
* [aws cli](https://aws.amazon.com/cli/)
* [poetry](https://python-poetry.org/)

## Assumption

Upon running the application, the following are assumed;

* Your infrastructure is AWS.
* You are using AWS ECR to store container builds.
* Your version control provider is Bitbucket, and we will use Bitbucket Pipeline for CI/CD.

## Run CI/CD

To run CI/CD pipeline, ensure the following in secrets/variables;

* AWS_SECRET_ACCESS_KEY
* AWS_ACCESS_KEY_ID
* AWS_REGION

Notes: Ensure that the AWS account has permission or role to the following:

* CreateObject and PutObject S3
* GetObject in S3
* GetAuthorizationToken ECR
* BatchGetImage to ECR

## Scripts

There are various scripts in the `scripts` folder to ensure ease.

Script includes

* `build_multiplatform.sh` -- Building docker container for multiplatform. Current builds are Linux/amd64 and Linux/arm64. After the build, the container is pushed to ECS.

    Notes: Ensure ECR is configured before. For configuration check the code below;

    ` aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 12345566.dkr.ecr.eu-west-1.amazonaws.com
`

    Change `12345566` to your AWS ACCOUNT ID.

* `lint.sh` -- Ensure that the following linters are applied to your codebase; [black](https://pypi.org/project/black/),  [mypy](https://mypy-lang.org/) and [pylint](https://pypi.org/project/pylint/).

* `tests.sh` -- Runs test and coverage using poetry and coverage.

* `run_locally.sh` -- Run your docker builds locally. In case you want to debug something.

## Run Application

As stated earlier, it is assumed that application will run on the AWS Ecosystems.

There are two ways to run this application:

1. Run `python xml_parser_service/main.py` (without any arguments) in the terminal or add to command in your Kubernetes manifest (see example below)

    ```json
    "command": [
        "/bin/sh",
        "-c",
        "python interaction_tool_service/main.py"
        ]
    ```

    However, `EVENTS`(triggered when an object is added to an S3 bucket) should be as an environment variable [see setting `EVENTS` as environment variable below].

    ```bash
    export EVENTS='{"Records": [{"eventVersion": "2.0", "eventSource": "aws:s3", "awsRegion": "us-east-1", "eventTime": "1970-01-01T00:00:00.000Z", "eventName": "ObjectCreated:Put", "userIdentity": {"principalId": "EXAMPLE"}, "requestParameters": {"sourceIPAddress": "127.0.0.1"}, "responseElements": {"x-amz-request-id": "EXAMPLE123456789", "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"}, "s3": {"s3SchemaVersion": "1.0", "configurationId": "testConfigRule", "bucket": {"name": "test-emile-dev", "ownerIdentity": {"principalId": "EXAMPLE"}, "arn": "arn:aws:s3:::example-bucket"}, "object": {"key": "sample.xml", "size": 1024, "eTag": "0123456789abcdef0123456789abcdef", "sequencer": "0A1B2C3D4E5F678901"}}}]}'
    ```

2. Run `python interaction_tool_service/main.py -e <EVENTS>`.

    `EVENTS` ==> object of type `str` that contains information of object added to S3 bucket.
