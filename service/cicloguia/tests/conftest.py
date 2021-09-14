from typing import List

import boto3
import pytest
from cicloguia.src import config
from cicloguia.src.adapters import repository
from cicloguia.src.domain import model

from uuid import uuid4
from typing import Dict


def random_id() -> str:
    return uuid4().hex


def random_product_data() -> Dict:
    return {
        'url': f'https://www.{random_id()}.cl',
        'product_name': f'fake_product_{random_id()}',
        'category': f'fake_category_{random_id()}',
        'brand': f'fake_brand_{random_id()}',
    }


@pytest.fixture(scope='module')
def random_product() -> model.Product:
    return model.Product(**random_product_data())


@pytest.fixture(scope='module')
def random_products() -> List:
    return [model.Product(**random_product_data()) for _ in range(0, 5)]


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
def image_names() -> List:
    return [
        '0b2834e9c236fb1103b23a457ed0f38af4cb51ff.jpg',
        '0c16a70bfa007df9e688c667e99b94ce97d7d4e7.jpg',
        '0c426e6409210db50d18010cdf8327afa11b5b4d.jpg',
    ]
