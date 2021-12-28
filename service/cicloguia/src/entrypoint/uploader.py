import json
import os
from typing import List, Dict

import boto3
from icecream import ic
from pydantic import ValidationError

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
    # the crossmountain-items.json lacks categories, breaking the execution since it is a secondary index
    # data_paths = ['../assets/crossmountain-items.json', '../assets/ridecl-items.json']
    data_paths = ['../assets/ridecl-items.json']
    products_data = []
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
                products_data.append(product)
            except ValidationError as error:
                ic(str(error))
                ic(raw_data)


if __name__ == '__main__':
    upload_products()
