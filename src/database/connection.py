from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from config import Config

db = create_engine(Config.DATABASE)
Base = declarative_base()
