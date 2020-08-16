import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

db_config = {
    "apiKey": "AIzaSyDIk3UNtPG28QHn84MWsWSexQjTpN9ibLs",
    "authDomain": "jpmc-45.firebaseapp.com",
    "databaseURL": "https://jpmc-45.firebaseio.com",
    "projectId": "jpmc-45",
    "storageBucket": "jpmc-45.appspot.com",
    "messagingSenderId": "916971610996",
    "serviceAccount": "app/serviceAccountKey.json"
}

# "appId": "1:916971610996:web:2474df09202ca5116a8221",
#         "measurementId": "G-BT2B9KWS05"