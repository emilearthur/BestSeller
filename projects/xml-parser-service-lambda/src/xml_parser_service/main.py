import json
import logging
import urllib.parse
from typing import Any, Dict, List, Union

from xml_parser_service.constant import PROCESSED_DATA_BUCKET
from xml_parser_service.exceptions import format_exception
from xml_parser_service import helpers
from xml_parser_service import s3_helper
from xml_parser_service.models import ProductData

logger = logging.getLogger("xml_parser_service")


def main_handler(event: Dict[str, Any]) -> Dict[str, Union[str, int]]:
    errors: List[Exception] = []
    processed_data: List[Dict[str, str]] = []

    if "Records" in event:
        records = event["Records"]

    for record in records:
        try:
            logger.info(
                "request received", extra={"request": json.dumps(record, default=str)}
            )
            bucket = record["s3"]["bucket"]["name"]
            key = urllib.parse.unquote_plus(
                record["s3"]["object"]["key"], encoding="utf-8"
            )

            logger.info("Data processing started")

            data = s3_helper.get_data_from_s3(bucket, key)

            items = helpers.load_xml(next(data))

            for item in items:
                processed_item = ProductData(
                    product_id=item.get("id"),
                    product_category=helpers.get_field_values(
                        item, "category", to_text=True
                    ),
                    product_description=helpers.get_field_values(
                        item, "description", to_text=True
                    ),
                    product_images=helpers.get_product_images(
                        helpers.get_field_values(item, "images")
                    ),
                    prices=helpers.get_product_prices(
                        helpers.get_field_values(item, "prices")
                    ),
                )
                processed_data.append(processed_item.dict())

            s3_helper.upload_to_s3(
                processed_data,
                PROCESSED_DATA_BUCKET,
                f"processed_{key}".replace(".xml", ".json")
            )

            logger.info("Data processing Done")

        except (KeyError, AttributeError, TypeError) as err:
            logger.error(err, exc_info=True)
            errors.append(err)

    if errors:
        return {
            "statusCode": 400,
            "body": json.dumps({"ETL Errored": format_exception(errors[0])}),
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"ETL Done": True}),
    }
