import os
import pyrebase

# FIREBASE CONFIG
config = {

  "apiKey": os.environ['FIREBASE_SECRET_KEY'],
  "authDomain": "campustutors-78ccb.firebaseapp.com",
  "databaseURL": "https://campustutors-78ccb.firebaseio.com",
  "storageBucket": "campustutors-78ccb.appspot.com",
  "serviceAccount": "app/secret.json"
}


# Service Authenticate
def connect_database():
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    return db
