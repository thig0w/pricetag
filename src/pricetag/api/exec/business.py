# -*- coding: utf-8 -*-
"""Business logic for /user API endpoints."""

import requests
from lxml import html
from sqlalchemy.orm import Session

from src.pricetag import models

# Headers to use in request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}


async def get_price_for_product(db: Session, product_id: int) -> int:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    page = requests.get(product.url, headers=headers)

    # Parsing the page
    # (We need to use page.content rather than
    # page.text because html.fromstring implicitly
    # expects bytes as input.)
    tree = html.fromstring(page.content)

    # Get element using XPath
    price_element = tree.xpath(product.xpath)
    try:
        price = price_element[0].text
    except IndexError:
        # Probably out of stock (element not found on page)
        price = -1
    return price
