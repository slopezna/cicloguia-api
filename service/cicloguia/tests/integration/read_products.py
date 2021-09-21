import boto3
from icecream import ic

from cicloguia.src import config
from cicloguia.src.adapters import repository

if __name__ == '__main__':
    dynamodb_session = boto3.resource('dynamodb', **config.get_dynamo_parameters(test=True))
    products_repo = repository.DynamoRepository(session=dynamodb_session)
    # products_repo.create_table()
    results = products_repo.get_by_category(category='ruedas')
    ic(results)
