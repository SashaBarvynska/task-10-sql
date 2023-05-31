import os
from dotenv.main import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE"]
    PORT = os.environ["APP_PORT"]
    HOST = os.environ["APP_HOST"]
    DEBUG = os.environ.get("debug", True)


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["TEST_DATABASE"]
    TESTING = os.environ.get("debug", True)
