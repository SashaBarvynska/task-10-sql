import os
from dotenv.main import load_dotenv

load_dotenv()


class Config:
    DATABASE = os.environ["DATABASE"]
    PORT = os.environ["APP_PORT"]
    HOST = os.environ["APP_HOST"]
    DEBUG = os.environ.get("debug", True)


class TestConfig(Config):
    TEST_DATABASE = os.environ["TEST_DATABASE"]
    TESTING = os.environ.get("debug", True)
