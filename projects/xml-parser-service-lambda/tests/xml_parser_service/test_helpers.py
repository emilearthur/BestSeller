from typing import Iterator, Dict, List

import boto3
from mypy_boto3_s3.client import S3Client
import bs4

from xml_parser_service.s3_helper import get_data_from_s3
from xml_parser_service.helpers import (
    load_xml,
    get_field_values,
    get_product_images,
    get_product_prices,
)

boto3.setup_default_session(profile_name="dev")


def s3_client() -> S3Client:
    return boto3.client(service_name="s3", region_name="eu-west-1")


def test_load_xml() -> None:
    data = get_data_from_s3(
        "test-emile-dev",
        "sample.xml",
        s3_client(),
    )
    assert isinstance(data, Iterator)

    datum = next(data)

    items = load_xml(datum)

    assert isinstance(items, bs4.element.ResultSet)

    assert len(items) == 2

    assert items[0].get("id") == "2445456"


def test_get_field_values() -> None:
    data = get_data_from_s3(
        "test-emile-dev",
        "sample.xml",
        s3_client(),
    )
    datum = next(data)
    items = load_xml(datum)

    product_category_tag = get_field_values(items[0], "category")
    assert isinstance(product_category_tag, bs4.element.Tag)

    product_category = product_category_tag.text
    assert product_category == "Jeans"


def test_get_field_values_to_text() -> None:
    data = get_data_from_s3(
        "test-emile-dev",
        "sample.xml",
        s3_client(),
    )
    datum = next(data)
    items = load_xml(datum)

    product_category = get_field_values(items[0], "category", to_text=True)
    assert not isinstance(product_category, bs4.element.Tag)
    assert isinstance(product_category, str)
    assert product_category == "Jeans"


def test_get_field_values_none() -> None:
    data = get_data_from_s3(
        "test-emile-dev",
        "sample.xml",
        s3_client(),
    )
    datum = next(data)
    items = load_xml(datum)

    product_category_tag = get_field_values(items[0], "tests")
    assert product_category_tag == ""


def test_get_product_images() -> None:
    data = get_data_from_s3(
        "test-emile-dev",
        "sample.xml",
        s3_client(),
    )
    datum = next(data)
    items = load_xml(datum)

    product_images = get_product_images(get_field_values(items[0], "images"))
    assert isinstance(product_images, Dict)

    assert (
        product_images.get("image_1") == "https://sample.com/img /2445456_Image_1.jpg"
    )


def test_get_product_prices() -> None:
    data = get_data_from_s3(
        "test-emile-dev",
        "sample.xml",
        s3_client(),
    )
    datum = next(data)
    items = load_xml(datum)

    product_prices = get_product_prices(get_field_values(items[0], "prices"))
    assert isinstance(product_prices, List)

    assert isinstance(product_prices[0], Dict)

    for key, value in product_prices[0].items():
        assert key == "EUR"
        assert value == "49.95"
