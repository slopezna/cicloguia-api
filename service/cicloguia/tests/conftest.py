import boto3
import pytest
from cicloguia.src import config
from cicloguia.src.adapters import repository
from cicloguia.src.domain import model
from cicloguia.tests import utils


@pytest.fixture(scope='module')
def random_product() -> model.Product:
    return model.Product(**utils.generate_random_product_data())


@pytest.fixture
def products_repo() -> repository.DynamoRepository:
    dynamodb_session = boto3.resource('dynamodb', **config.get_dynamo_parameters(test=True))
    products_repo = repository.DynamoRepository(session=dynamodb_session)
    products_repo.create_table()
    return products_repo
