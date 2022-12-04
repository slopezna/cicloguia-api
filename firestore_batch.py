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

    batch = db.batch()

    data = {
        u'name': u'Los Angeles',
        u'state': u'CA',
        u'country': u'USA'
    }
    nyc_ref = db.collection(u'cities').document(u'NYC')
    batch.set(nyc_ref, data)
    batch.commit()
