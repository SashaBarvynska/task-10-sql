from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

db = create_engine(Config.DATABASE)
Base = declarative_base()
Session = sessionmaker(bind=db)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except DatabaseError:
        session.rollback()
    finally:
        session.close()
