from cicloguia.src.domain import model

"""
class Product(BaseModel):
    url: str
    product_name: str
    category: str
    brand: str
    sku: Optional[int]
    price: Optional[str]
    description: Optional[str]
    specifications: Optional[str]  # technical specifications
    alert: Optional[str]  # could be either oos or pre-sale
    sizes: Optional[List[str]]
    unavailable_sizes: Optional[List[str]]
    image_urls: Optional[List[str]]
"""


def test_model_instance(random_product: model.Product):
    assert isinstance(random_product, model.Product)
    assert random_product.image_urls is None
