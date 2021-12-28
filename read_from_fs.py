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
        os.environ['FIRESTORE_DATASET'] = 'test'
        os.environ['FIRESTORE_EMULATOR_HOST'] = 'localhost:8001'
        os.environ['FIRESTORE_EMULATOR_HOST_PATH'] = 'localhost:8001/firestore'
        os.environ['FIRESTORE_HOST'] = 'http://localhost:8001'
        os.environ['FIRESTORE_PROJECT_ID'] = 'test'

        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        db = firestore.Client(project='test', credentials=credentials)

    doc_ref = db.collection(u'cities').document(u'LA')

    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print(u'No such document!')
