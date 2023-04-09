import functools
import os

import boto3
from mypy_boto3_s3.client import S3Client

REGION_NAME: str = os.environ.get("REGION_NAME", "eu-west-1")

PROCESSED_DATA_BUCKET = os.environ.get("PROCESSED_DATA_BUCKET", "test-emile-dev")


@functools.cache
def s3_client() -> S3Client:
    return boto3.client(service_name="s3", region_name=REGION_NAME)


APPLICATIONS = ["xml_parser_service", "helpers", "s3_helper"]
