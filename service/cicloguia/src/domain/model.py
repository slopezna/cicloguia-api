from typing import List, Optional

from pydantic import BaseModel


class Product(BaseModel):
    url: str
    product_name: str
    brand: str
    category: str
    sku: Optional[int]
    price: Optional[str]
    description: Optional[str]
    specifications: Optional[str]  # technical specifications
    alert: Optional[str]  # could be either oos or pre-sale
    sizes: Optional[List[str]]
    unavailable_sizes: Optional[List[str]]
    image_urls: Optional[List[str]]

    def __repr__(self) -> str:
        return f'<Product: {self.url}>'
