import os
import pyrebase
from decouple import config
import firebase_admin
from firebase_admin import credentials

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cred = credentials.Certificate(os.path.join(BASE_DIR, "../package-lock.json"))
firebase_admin.initialize_app(cred)

FIREBASE_CONFIG = {
    "apiKey": config("FIREBASE_API_KEY"),
    "authDomain": config("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": config("FIREBASE_DATABASE_URL"),
    "projectId": config("FIREBASE_PROJECT_ID"),
    "storageBucket": config("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": config("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": config("FIREBASE_APP_ID"),
}

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
db = firebase.database()