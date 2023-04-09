import argparse
import ast
import json
import logging
import os
import sys
import urllib.parse
from typing import Any, Dict, List

from xml_parser_service import helpers, s3_helper
from xml_parser_service.constant import APPLICATIONS, PROCESSED_DATA_BUCKET
from xml_parser_service.exceptions import format_exception
from xml_parser_service.models import ProductData

logger = logging.getLogger("xml_parser_service")

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


def main(events: Dict[str, Any]) -> None:
    logger.info(
        "Start ETL to parse XML data",
        extra={
            "event": events,
        },
    )

    processed_data: List[Dict[str, str]] = []

    if "Records" in events:
        records = events["Records"]

    for record in records:
        try:
            logger.info(
                "request received",
                extra={"request": json.dumps(record, default=str)},
            )
            bucket = record["s3"]["bucket"]["name"]
            key = urllib.parse.unquote_plus(
                record["s3"]["object"]["key"], encoding="utf-8"
            )
            print(bucket, key)

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
                f"processed_{key}".replace(".xml", ".json"),
            )

            logger.info("Data processing Done")

        except (KeyError, AttributeError, TypeError) as err:
            logger.info(
                "Error Getting Contact on XCally",
                extra={"error": format_exception(err)},
                exc_info=True,
            )


if __name__ == "__main__":
    root_logger = logging.getLogger("")
    if not root_logger.handlers:
        root_logger.addHandler(logging.StreamHandler(sys.stdout))

    for name in APPLICATIONS:
        logging.getLogger(name).setLevel(LOG_LEVEL)

    argparser = argparse.ArgumentParser(description="Args for Interaction Service")
    argparser.add_argument("-e", "--events", default=os.environ.get("EVENTS"), type=str)

    args = argparser.parse_args()
    if (args.events is None) or (args.events == ""):
        logger.info("Event can either be parsed or as an environment variable.")
    else:
        main(events=ast.literal_eval(args.events))
