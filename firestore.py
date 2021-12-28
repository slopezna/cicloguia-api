import os

import google.auth.credentials
import mock
from google.cloud import firestore

if __name__ == '__main__':
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

        data = {
            u'name': u'Los Angeles',
            u'state': u'CA',
            u'country': u'USA'
        }

        # Add a new doc in collection 'cities' with ID 'LA'
        db.collection(u'products').document(u'LA').set(data)
