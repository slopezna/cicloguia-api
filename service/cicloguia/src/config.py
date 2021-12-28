import os
from typing import Dict


def get_firestore_collection() -> str:
    return os.getenv('FIRESTORE_COLLECTION', 'items')


def get_s3_parameters(test: bool = False) -> Dict:
    if test:
        dev_config = {
            'endpoint_url': 'http://localhost:4000',
            'region_name': 'us-east-1',
        }
    else:
        dev_config = {
            'endpoint_url': 'http://s3:4566',
            'region_name': 'us-east-1',
        }
    prod_config = {}
    return dev_config if os.getenv('APP_ENV', default='development') == 'development' else prod_config


def get_bucket_name(test: bool = False) -> str:
    return 'testing-products' if test else os.getenv('S3_BUCKET', default='products')
