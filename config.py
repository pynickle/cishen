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
SQLALCHEMY_DATABASE_URI = "postgres://imbfeplizqnifh:fe5383bed6e0433eec1894e94170341d8df048d2f3f2e0543ce1a19d5a7b04c0@ec2-54-83-36-37.compute-1.amazonaws.com:5432/d82e3li2tn8df0"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = {
    'wrongwords': "postgres://rmoupqnsllwcwb:4c3049a0bc7ddd7feb0bf4427c0df7bd17da25e319136287db8d748a38f20834@ec2-50-19-114-27.compute-1.amazonaws.com:5432/dc52vkcmqrgohg",
    "github-users": "postgres://dcsjeaileydpus:e180afd4b693d93db0ab6d36df480a30d60f052ed1ea0e9f9a6258cdb9810856@ec2-184-72-238-22.compute-1.amazonaws.com:5432/dctr8f4c3hj0eg",
    "admin-users": "postgres://imbfeplizqnifh:fe5383bed6e0433eec1894e94170341d8df048d2f3f2e0543ce1a19d5a7b04c0@ec2-54-83-36-37.compute-1.amazonaws.com:5432/d82e3li2tn8df0"
}