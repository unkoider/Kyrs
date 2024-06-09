import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1@localhost/mobym_game'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
