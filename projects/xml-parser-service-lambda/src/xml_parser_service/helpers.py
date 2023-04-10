import logging
from typing import Dict, List, Union

import bs4
from bs4 import BeautifulSoup

logger = logging.getLogger("helpers")


def get_field_values(
    item: bs4.element.Tag, value: str, to_text: bool = False
) -> Union[str, bs4.element.Tag]:
    output = item.findChild(value)
    if isinstance(output, bs4.element.Tag):
        if to_text:
            return output.text
        return output

    return ""


def get_product_images(item: bs4.element.Tag) -> Dict[str, str]:
    images: Dict[str, str] = {}
    for image_data in item:
        if isinstance(image_data, bs4.element.Tag):
            images.update({f"image_{image_data.get('type')}": image_data.get("url")})

    return images


def get_product_prices(item: bs4.element.Tag) -> List[Dict[str, str]]:
    prices_list: List[Dict[str, str]] = []

    for price in item:
        if isinstance(price, bs4.element.Tag):
            output = price.text.split()
            currency, value = output[0], output[1]
            prices_list.append({currency: value})

    return prices_list


def load_xml(data_bytes: bytes) -> bs4.element.ResultSet:
    logger.info("loading xml data")

    data = data_bytes.decode("utf-8")
    soup = BeautifulSoup(data, "xml")

    items = soup.find_all("item")

    return items
