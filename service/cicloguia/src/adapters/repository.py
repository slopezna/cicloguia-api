import logging
from typing import Dict, Optional

from botocore.exceptions import ClientError
from botocore.response import StreamingBody
from cicloguia.src import config
from cicloguia.src.domain.model import Product


class DynamoRepository:
    def __init__(self, session, table_name: str = config.get_dynamo_table_name()):
        self.session = session
        self.table_name = table_name
        self.table = self.session.Table(self.table_name)
        self.read_capacity_units = 10
        self.write_capacity_units = 10

    def add(self, item: Product) -> Dict:
        return self.table.put_item(Item=item.__dict__)

    # todo: implement this feature
    def bulk_insert(self):
        pass

    def get(self, url: str) -> Optional[Product]:
        try:
            response = self.table.get_item(Key={'url': url})
        except ClientError as error:
            logging.error(error.response['Error']['Message'])
        else:
            try:
                return Product(**response['Item'])
            except KeyError:
                return None

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
