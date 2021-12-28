import logging
from typing import Dict, Optional

# noinspection PyPackageRequirements
from botocore.exceptions import ClientError
# noinspection PyPackageRequirements
from botocore.response import StreamingBody

from cicloguia.src import config


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
