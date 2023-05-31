from contextlib import contextmanager
from sqlalchemy.exc import DatabaseError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session


db = SQLAlchemy()


@contextmanager
def get_session():
    session: Session = db.session
    try:
        yield session
        session.commit()
    except DatabaseError:
        session.rollback()
    finally:
        session.close()
