import os
from flask import Config
from dotenv import load_dotenv
load_dotenv()


class ProductionConfig(Config):
    DB_NAME = os.environ.get("DB_NAME")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    SECRET = os.environ.get("SALT")


class TestingConfig(Config):
    DB_NAME = 'mongoenginetest'
    DB_HOST = "mongomock://localhost",
    DB_PORT = os.environ.get("DB_PORT")
    SECRET = os.environ.get("SALT")


class DevelopmentConfig(Config):
    DB_NAME = os.environ.get("DB_NAME")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    SECRET = os.environ.get("SALT")