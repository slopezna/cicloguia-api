import os

import google.auth.credentials
import mock
from fastapi import FastAPI
from google.cloud import firestore
from icecream import ic

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
    record = db.collection('products').document('tiendaride.cl/product/bicicleta-polygon-xtrada-5-2021').get()
    return record.to_dict(), 200


@app.get("/items")
def read_item():
    docs = db.collection('products').stream()

    for doc in docs:
        ic(f'{doc.id} => {doc.to_dict()}')

    return 'ok', 200


@app.get("/images/{name}")
def read_image(name: str):
    return {"item_id": name}
