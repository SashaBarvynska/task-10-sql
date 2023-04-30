from sqlalchemy.orm import Session


class BaseReporistory:
    def __init__(self, session: Session):
        self.session: Session = session
