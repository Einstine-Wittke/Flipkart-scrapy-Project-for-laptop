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

def extract_original_price(value) -> str:
    """Extract original price - handles strings or elements."""
    if not value:
        return "No Original Price"
    
    # If it's a string, return it
    if isinstance(value, str):
        value = value.strip()
        return value if value else "No Original Price"
    
    # If it's an element object with inner_text method
    if hasattr(value, 'inner_text'):
        try:
            text = value.inner_text()
            return text.strip() if text else "No Original Price"
        except:
            return "No Original Price"
    
    return "No Original Price"

def extract_discount(value) -> str:
    """Extract discount text - handles strings or element objects."""
    
    if not value:
        return "No Discount"
    
    # If already a string
    if isinstance(value, str):
        value = value.strip()
        return value if value else "No Discount"
    
    # If it's an element (Playwright element handle)
    if hasattr(value, 'inner_text'):
        try:
            text = value.inner_text()
            return text.strip() if text else "No Discount"
        except:
            return "No Discount"
    
    return "No Discount"


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
        input_processor= MapCompose(float),
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
    output_processor=extract_details
    )

    pass
