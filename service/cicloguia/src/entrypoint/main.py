import os

import google.auth.credentials
import mock
from fastapi import FastAPI
from google.cloud import firestore

app = FastAPI()

# noinspection DuplicatedCode
if os.getenv('GAE_ENV', '').startswith('standard'):
    # production
    db = firestore.Client()
else:
    # localhost
    os.environ['FIRESTORE_DATASET'] = 'test'
    os.environ['FIRESTORE_EMULATOR_HOST'] = 'localhost:8001'
    os.environ['FIRESTORE_EMULATOR_HOST_PATH'] = 'localhost:8001/firestore'
    os.environ['FIRESTORE_HOST'] = 'http://localhost:8001'
    os.environ['FIRESTORE_PROJECT_ID'] = 'test'

    credentials = mock.Mock(spec=google.auth.credentials.Credentials)

    # noinspection PyTypeChecker
    db = firestore.Client(project='test', credentials=credentials)


@app.get("/")
def read_root():
    return 200


@app.get("/items/{category}")
def read_item(category: str):
    return {"item_id": category}


@app.get("/images/{name}")
def read_image(name: str):
    return {"item_id": name}
