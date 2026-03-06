# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# use processors from the standalone itemloaders package
from itemloaders.processors import MapCompose, TakeFirst
import re
from itemloaders.processors import Identity

price_re = re.compile(r"[^\d,]+")

def clean_price(txt: str) -> float:
    """Extract and convert price string to float."""
    if not txt or not isinstance(txt, str):
        return 0.0
    clean = price_re.sub("", txt)
    try:
        return float(clean.replace(",", ""))
    except ValueError:
        return 0.0

def format_price(txt: str) -> str:
    """Format price as currency string with comma separators."""
    return f"{clean_price(txt):,.2f}"

def clean_rating(value):
    try:
        return float(value)
    except:
        return 0.0

def extract_original_price(value):
    if not value:
        return 0.0
    return clean_price(value)

def extract_discount(value):
    if not value:
        return "0%"

    if isinstance(value, str):
        value = value.strip()
        return value if value else "0%"

    return "0%"


def extract_details(values): 
    if not values: 
        return {"details": []} 
    return {"details": [v.strip() for v in values if v]}


class LaptopItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(
        input_processor= MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor= MapCompose(clean_price),
        output_processor=TakeFirst()
    )
    rating = scrapy.Field(
    input_processor=MapCompose(clean_rating),
    output_processor=TakeFirst()
    )
    
    original_price = scrapy.Field(
        input_processor= MapCompose(clean_price),
        output_processor=TakeFirst()
    )
    discount = scrapy.Field(
    input_processor=MapCompose(extract_discount),
    output_processor=TakeFirst()
    )
    details = scrapy.Field(
    input_processor=MapCompose(str.strip),
    output_processor=extract_details
    )

    pass
