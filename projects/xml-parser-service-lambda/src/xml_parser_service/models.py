# pylint: disable=no-name-in-module

from typing import Dict, List

from pydantic import BaseModel


class ProductData(BaseModel):
    product_id: str
    product_category: str
    product_description: str
    product_images: Dict[str, str]
    prices: List[Dict[str, str]]
