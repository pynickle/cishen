import os
from datetime import timedelta


client_id = '5dc32030b7b77a72564b'
client_secret = '75b7099bed808db672af0be0d79d0e940813ca06'

SECRET_KEY = os.urandom(24)
SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
PERMANENT_SESSION_LIFETIME = timedelta(days = 365)
GITHUB_CLIENT_ID = client_id
GITHUB_CLIENT_SECRET = client_secret
SQLALCHEMY_DATABASE_URI = 'sqlite:///words.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = {
    'wrongwords': 'sqlite:///wrongwords.sqlite3',
    "users": "sqlite:///users.sqlite3"
}