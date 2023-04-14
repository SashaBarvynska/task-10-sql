import os


class Config:
    DATABASE = os.environ.get('DATABASE', 'DB_URL')
    DEBUG = os.environ.get('debug', True)
