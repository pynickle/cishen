import os
from datetime import timedelta


client_id = '5dc32030b7b77a72564b'
client_secret = '75b7099bed808db672af0be0d79d0e940813ca06'

SECRET_KEY = os.urandom(24)
SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
PERMANENT_SESSION_LIFETIME = timedelta(days = 365)
GITHUB_CLIENT_ID = client_id
GITHUB_CLIENT_SECRET = client_secret
"""
SQLALCHEMY_DATABASE_URI = 'sqlite:///words.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = {
    'wrongwords': 'sqlite:///wrongwords.sqlite3',
    "users": "sqlite:///users.sqlite3"
}
"""
SQLALCHEMY_DATABASE_URI = "postgres://duxozyvlrdpiby:498cde3f5512141a7a520935e5045d553cfc9e5fbe1f0bb5e87216412dafce8d@ec2-174-129-240-67.compute-1.amazonaws.com:5432/dc6jn5i3h0l9vs"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = {
    'wrongwords': "postgres://orekhscplkyxys:bc834760315438a684a3f0183799f337098a27a8d2112b09979471e4f2c583af@ec2-174-129-240-67.compute-1.amazonaws.com:5432/d1ui0dg4kkb9n7",
    "github-users": "postgres://xruniacvftyjcu:24ed9fe80e22832a89cfd62e63f756346ce0b8783753e72c3731142f12f2893a@ec2-50-19-114-27.compute-1.amazonaws.com:5432/d4hrri9ea2p525",
    "admin-users": "postgres://ipyejdahvfvdar:72ef8bc88376f5a84e8d83345bc0116b8bfeef34df04518f0180c6397e52e1d0@ec2-174-129-240-67.compute-1.amazonaws.com:5432/de0t54s95v8kkn"
}