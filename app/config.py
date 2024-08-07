import os
import firebase_admin
from firebase_admin import credentials

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(BASE_DIR, '../package_log.json'))
connection = firebase_admin.initialize_app(cred)