import os
import pyrebase
import json

# FIREBASE CONFIG
config = {

  "apiKey": os.environ['FIREBASE_SECRET_KEY'],
  "authDomain": "campustutors-78ccb.firebaseapp.com",
  "databaseURL": "https://campustutors-78ccb.firebaseio.com",
  "storageBucket": "campustutors-78ccb.appspot.com",
  "serviceAccount": "app/secret.json"
}

firebase = pyrebase.initialize_app(config)


# Service Authenticate
def connect_database():

    db = firebase.database()

    return db


def authenticate_user(email, password):
    auth = firebase.auth()
    database = connect_database()
    user = auth.create_user_with_email_and_password(email, password)

    return user['idToken']


def login_user(email, password):
    auth = firebase.auth()
    database = connect_database()

    user = auth.sign_in_with_email_and_password(email, password)

    return user
