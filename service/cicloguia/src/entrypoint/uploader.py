import json
import os
from typing import List, Dict

import boto3
import google.auth.credentials
import mock
from google.api_core.exceptions import InvalidArgument
from google.cloud import firestore
from icecream import ic

from cicloguia.src import config
from cicloguia.src.adapters import repository
from cicloguia.src.domain import model


def upload_images() -> None:
    images_folders: List = [
        {
            'os_path': '../assets/crossmountain/full/',
            's3_path': 'assets/crossmountain/full/'
        },
        {
            'os_path': '../assets/ridecl/full/',
            's3_path': 'assets/ridecl/full/'
        },
    ]
    s3_session = boto3.client('s3', **config.get_s3_parameters(test=True))
    images_repo = repository.S3Repository(session=s3_session)
    images_repo.create_bucket()
    for item in images_folders:
        for (_, _, file_names) in os.walk(item['os_path']):
            for file_name in file_names:
                full_path = item['os_path'] + file_name
                full_s3_path = item['s3_path'] + file_name
                with open(full_path, 'rb') as data:
                    images_repo.add(data=data, file_name=full_s3_path)


def upload_products() -> None:
    if os.getenv('GAE_ENV', '').startswith('standard'):
        # production
        db = firestore.Client()
    else:
        # localhost
        # noinspection DuplicatedCode
        os.environ['FIRESTORE_DATASET'] = 'test'
        os.environ['FIRESTORE_EMULATOR_HOST'] = 'localhost:8001'
        os.environ['FIRESTORE_EMULATOR_HOST_PATH'] = 'localhost:8001/firestore'
        os.environ['FIRESTORE_HOST'] = 'http://localhost:8001'
        os.environ['FIRESTORE_PROJECT_ID'] = 'test'

        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        # noinspection PyTypeChecker
        db = firestore.Client(project='test', credentials=credentials)

    batch = db.batch()

    # the crossmountain-items.json lacks categories, breaking the execution since it is a secondary index
    # data_paths = ['../assets/crossmountain-items.json', '../assets/ridecl-items.json']
    data_paths = ['../assets/ridecl-items.json']

    for path in data_paths:
        for line in open(path, 'r'):
            # todo: create a cleaning function with regex instead of ifs
            raw_data: Dict = {}
            try:
                raw_data = json.loads(line)
                for key, item in raw_data.items():
                    if len(item) == 1:
                        raw_data[key] = item[0]
                    elif len(item) == 0:
                        raw_data[key] = None
                    else:
                        if key == 'specifications':
                            raw_data[key] = ' '.join(item)
                        if key == 'product_name':
                            raw_data[key] = item[0]

                product = model.Product(**raw_data)
                nyc_ref = db.collection('products').document(product.url.replace('https://', ''))
                batch.set(nyc_ref, product._asdict())
            except InvalidArgument as error:
                ic(str(error))
                ic(raw_data)

    batch.commit()


if __name__ == '__main__':
    upload_products()
