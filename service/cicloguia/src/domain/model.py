from typing import List, Optional

from pydantic import BaseModel


class Product(BaseModel):
    url: Optional[str]
    sku: Optional[int]
    product_name: Optional[str]
    brand: Optional[str]
    category: Optional[str]
    price: Optional[str]
    description: Optional[str]
    specifications: Optional[str]  # technical specifications
    alert: Optional[str]  # could be either oos or pre-sale
    sizes: Optional[List[str]]
    unavailable_sizes: Optional[List[str]]
    image_urls: Optional[List[str]]
