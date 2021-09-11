from typing import Dict

from cicloguia.src.adapters import repository
from cicloguia.src.domain import model
from cicloguia.tests import utils


def test_insert_product(random_product: model.Product, products_repo: repository.DynamoRepository) -> None:
    response = products_repo.add(item=random_product)
    assert isinstance(response, Dict)


def test_get_product(random_product: model.Product, products_repo: repository.DynamoRepository) -> None:
    response = products_repo.get(url=random_product.url)
    assert isinstance(response, model.Product)


def test_missing_product(products_repo: repository.DynamoRepository) -> None:
    random_url = utils.generate_random_product_data()['url']
    response = products_repo.get(url=random_url)
    assert not response
