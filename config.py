import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE")
    PORT = os.getenv("APP_PORT")
    HOST = os.getenv("APP_HOST")
    DEBUG = os.getenv("debug", True)


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE")
    TESTING = os.getenv("debug", True)
