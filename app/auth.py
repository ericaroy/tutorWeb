import os
import pyrebase

# FIREBASE CONFIG
config = {

  "apiKey": os.environ['FIREBASE_SECRET_KEY'],
  "authDomain": "campustutors-78ccb.firebaseapp.com",
  "databaseURL": "https://campustutors-78ccb.firebaseio.com",
  "storageBucket": "campustutors-78ccb.appspot.com",
  "serviceAccount": {
        'client_email': os.environ['FIREBASE_CLIENT_EMAIL'],
        'client_id': os.environ['FIREBASE_CLIENT_ID'],
        'private_key': os.environ['FIREBASE_PRIVATE_KEY'].replace('\\n', '\n'),
        'private_key_id': os.environ['FIREBASE_PRIVATE_KEY_ID'],
        'type': 'service_account'
    }
}


# Service Authenticate
def connect_database():
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    return db
