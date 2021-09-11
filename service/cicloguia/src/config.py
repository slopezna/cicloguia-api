import os


def get_dynamo_parameters():
    dev_config = {
        'endpoint_url': 'http://dynamodb:8000',
        'region_name': 'us-east-1',
    }
    prod_config = {
        'region_name': 'us-east-1'
    }
    return dev_config if os.getenv('APP_ENV', default='development') == 'development' else prod_config


def get_dynamo_table_name():
    return os.getenv('DYNAMODB_TABLE', default='products')


def get_s3_parameters():
    dev_config = {
        'endpoint_url': 'http://s3:4566',
        'region_name': 'us-east-1',
    }
    prod_config = {}
    return dev_config if os.getenv('APP_ENV', default='development') == 'development' else prod_config


def get_bucket_name():
    return os.getenv('S3_BUCKET', default='products')
