from datetime import datetime
from typing import Iterator

import pytest
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client

from xml_parser_service.s3_helper import get_data_from_s3, split_s3_path, upload_to_s3


def test_get_data_from_s3(s3_client: S3Client) -> None:
    data = get_data_from_s3(
        "test-emile-dev",
        "sample.xml",
        s3_client,
    )
    assert isinstance(data, Iterator)

    datum = next(data)
    assert isinstance(datum, bytes)


def test_get_data_from_s3_error_nobucket(s3_client: S3Client) -> None:
    with pytest.raises(StopIteration):
        data = get_data_from_s3(
            "test-emile-devkk", "2023-04-07_22_50_13.json", s3_client
        )
        next(data)


def test_get_data_from_s3_error_nokey(s3_client: S3Client) -> None:
    with pytest.raises(StopIteration):
        data = get_data_from_s3(
            "test-emile-dev",
            "2023-04-07_22_50_13ap.json",
            s3_client,
        )

        next(data)


def test_get_data_from_s3_error_s3_client(s3_client_wrong: S3Client) -> None:
    with pytest.raises(ClientError):
        data = get_data_from_s3(
            "test-emile-dev",
            "2023-04-07_22_50_13.json",
            s3_client_wrong,
        )

        next(data)


def test_split_s3_path() -> None:
    s3_url = "s3://test-emile-dev/2023-04-07_22_50_13.json"
    bucket, key = split_s3_path(s3_url)
    assert bucket == "test-emile-dev"
    assert key == "2023-04-07_22_50_13.json"


def test_split_s3_path_err() -> None:
    with pytest.raises(AttributeError):
        split_s3_path(None)


def test_upload_to_s3(s3_client: S3Client) -> None:
    processed_data = [
        {
            "product_id": "2445456",
            "product_category": "Jeans",
            "product_description": "Bootleg Front Washed",
            "product_images": {
                "image_1": "https://sample.com/img /2445456_Image_1.jpg",
                "image_3": "https://sample.com/img /2445456_Image_3.jpg",
            },
            "prices": [{"EUR": "49.95"}, {"DKK": "445.60"}],
        },
        {
            "product_id": "2445456",
            "product_category": "Jeans",
            "product_description": "Bootleg Front Washed",
            "product_images": {
                "image_1": "https://sample.com/img /2445456_Image_1.jpg",
                "image_2": "https://sample.com/img /2445456_Image_2.jpg",
            },
            "prices": [{"EUR": "49.95"}, {"DKK": "445.60"}],
        },
    ]
    upload_to_s3(
        processed_data,
        "test-emile-dev",
        f"{datetime.now().strftime('%Y-%m-%d_%H_%M')}.json",
        s3_client,
    )

    data = get_data_from_s3(
        "test-emile-dev",
        f"{datetime.now().strftime('%Y-%m-%d_%H_%M')}.json",
        s3_client,
    )
    assert isinstance(data, Iterator)

    datum = next(data)
    assert isinstance(datum, bytes)
