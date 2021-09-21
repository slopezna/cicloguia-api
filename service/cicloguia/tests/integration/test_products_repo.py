from typing import Dict

from cicloguia.src.adapters import repository
from cicloguia.src.domain import model
from icecream import ic


def test_insert_product(random_product: model.Product, products_repo: repository.DynamoRepository):
    response = products_repo.add(item=random_product)
    assert isinstance(response, Dict)


def test_get_product(random_product: model.Product, products_repo: repository.DynamoRepository):
    product = products_repo.get_by_url(url=random_product.url)
    assert isinstance(product, model.Product)


def test_missing_product(products_repo: repository.DynamoRepository):
    assert products_repo.get_by_url(url='non_existing_url') is None


def test_batch_insert(random_products, products_repo: repository.DynamoRepository):
    assert products_repo.batch_insert(items=random_products) is None


def test_get_product_from_batch(random_products, products_repo: repository.DynamoRepository):
    product = products_repo.get_by_url(url=random_products[0].url)
    assert isinstance(product, model.Product)


def test_get_products_by_category(products_repo: repository.DynamoRepository):
    pass
    # ic(products_repo.get_by_category(''))
