import logging
import sys
import os
from typing import Any, Dict, Union

from xml_parser_service.main import main_handler
from xml_parser_service.constant import APPLICATIONS

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logger = logging.getLogger("xml_parser_service")

root_logger = logging.getLogger("")
if not root_logger.handlers:
    root_logger.addHandler(logging.StreamHandler(sys.stdout))

for name in APPLICATIONS:
    logging.getLogger(name).setLevel(LOG_LEVEL)


# pylint: disable=unused-argument
def handler(event: Dict[str, Any], context: Any) -> Dict[str, Union[str, int]]:
    logger.debug(
        "Start ETL to parse XML data",
        extra={
            "event": event,
        },
    )
    return main_handler(event)