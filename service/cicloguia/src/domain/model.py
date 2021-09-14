from typing import List, Optional, Union

from pydantic import BaseModel


class Product(BaseModel):
    url: str
    product_name: str
    brand: str
    category: Optional[str]
    sku: Union[int, str, None]
    price: Union[int, str, float, None]
    description: Optional[str]
    specifications: Optional[str]  # technical specifications
    alert: Union[List, str, None]  # could be either oos or pre-sale
    sizes: Union[List[str], str, None]
    unavailable_sizes: Union[List, str, None]
    image_urls: Union[List, str, None]

    def __repr__(self) -> str:
        return f'<Product: {self.url}>'
