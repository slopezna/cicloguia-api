import boto3
import pytest
from cicloguia.src import config
from cicloguia.src.adapters import repository
from cicloguia.src.domain import model
from cicloguia.tests import utils


@pytest.fixture(scope='module')
def random_product() -> model.Product:
    return model.Product(**utils.generate_random_product_data())


@pytest.fixture(scope='module')
def products_repo() -> repository.DynamoRepository:
    dynamodb_session = boto3.resource('dynamodb', **config.get_dynamo_parameters(test=True))
    products_repo = repository.DynamoRepository(
        session=dynamodb_session,
        table_name=config.get_dynamo_table_name(test=True)
    )
    products_repo.create_table()
    return products_repo


@pytest.fixture(scope='module')
def images_repo() -> repository.S3Repository:
    s3_session = boto3.client('s3', **config.get_s3_parameters(test=True))
    images_repo = repository.S3Repository(session=s3_session, bucket=config.get_bucket_name(test=True))
    images_repo.create_bucket()
    return images_repo


@pytest.fixture
def images_folder() -> str:
    return 'tests/integration/test_images/'


@pytest.fixture
def test_image_name() -> str:
    return '0b2834e9c236fb1103b23a457ed0f38af4cb51ff.jpg'
