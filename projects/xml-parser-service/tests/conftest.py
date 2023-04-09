import boto3
import pytest
from mypy_boto3_s3.client import S3Client

boto3.setup_default_session(profile_name="dev")


@pytest.fixture(scope="session", name="s3_client_wrong")
def s3_client_wrong() -> S3Client:
    return boto3.client(
        service_name="s3",
        aws_access_key_id="abcdeffgggh",
        aws_secret_access_key="12kk2mmddkkkdkakksssdsa",
        region_name="eu-west-1",
    )


@pytest.fixture(scope="session", name="s3_client")
def s3_client() -> S3Client:
    return boto3.client(service_name="s3", region_name="eu-west-1")
