import os


class Config:
    DATABASE = os.environ.get('DATABASE', 'postgresql://postgres:0672934823a@localhost:5432/postgres')
    DEBUG = os.environ.get('debug', True)


class TestConfig(Config):
    TESTING = os.environ.get('TESTING', True)
    TEST_DATABASE = os.environ.get('DATABASE', 'postgresql://postgres:0672934823a@localhost:5432/postgres')