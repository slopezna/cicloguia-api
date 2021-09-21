import logging
from typing import Dict, Optional, List

# noinspection PyPackageRequirements
from botocore.exceptions import ClientError
# noinspection PyPackageRequirements
from botocore.response import StreamingBody

from cicloguia.src import config
from cicloguia.src.domain.model import Product
from boto3.dynamodb.conditions import Key, Attr


# todo: create a pagination function
class DynamoRepository:
    def __init__(self, session, table_name: str = config.get_dynamo_table_name()):
        self.session = session
        self.table_name = table_name
        self.table = self.session.Table(self.table_name)
        self.read_capacity_units = 10
        self.write_capacity_units = 10

    def add(self, item: Product) -> Dict:
        return self.table.put_item(Item=item.__dict__)

    def batch_insert(self, items: List[Product]) -> None:
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item.__dict__)

    def get_by_url(self, url: str) -> Optional[Product]:
        try:
            response = self.table.get_item(Key={'url': url})
        except ClientError as error:
            logging.error(error.response['Error']['Message'])
        else:
            try:
                return Product(**response['Item'])
            except KeyError:
                return None

    def get_by_category(self, category: str):
        return self.table.query(IndexName='category', KeyConditionExpression=Key('category').eq(category))

    def update(self, item: Product) -> Dict:
        return self.add(item=item)

    def create_table(self) -> Dict:
        try:
            table = self.session.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'url',
                        'KeyType': 'HASH'  # Partition key
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'url',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'category',
                        'AttributeType': 'S'
                    },
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'category',
                        'KeySchema': [
                            {
                                'AttributeName': 'category',
                                'KeyType': 'HASH'
                            },
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 1,
                            'WriteCapacityUnits': 1,
                        }
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': self.read_capacity_units,
                    'WriteCapacityUnits': self.write_capacity_units
                }
            )
            return table

        except ClientError:
            logging.info('the DynamoDB table was already created!')


class S3Repository:
    def __init__(self, session, bucket: str = config.get_bucket_name()):
        self.session = session
        self.bucket_name = bucket

    def add(self, data, file_name: str) -> Dict:
        return self.session.upload_fileobj(Fileobj=data, Bucket=self.bucket_name, Key=file_name)

    def get(self, file_name: str) -> Optional[StreamingBody]:
        try:
            data: Dict = self.session.get_object(Bucket=self.bucket_name, Key=file_name)
            return data['Body']
        except ClientError as error:
            if error.response['Error']['Code'] == 'NoSuchKey':
                logging.info(f'file name: {file_name} not found')
                return None
            else:
                raise

    def create_bucket(self) -> None:
        self.session.create_bucket(Bucket=self.bucket_name)
