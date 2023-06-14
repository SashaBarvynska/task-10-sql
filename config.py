import os
from dotenv.main import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", None)
    PORT = os.getenv("APP_PORT", None)
    HOST = os.getenv("APP_HOST", None)
    DEBUG = os.getenv("debug", True)


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE", None)
    TESTING = os.getenv("debug", True)
