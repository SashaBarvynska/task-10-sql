from src.database.repositories.groups import GroupRepository
from src.database.connection import db
from src.database.models import GroupModel


def valid_format_of_data(data):
    return [{"id": i.id, "name": i.name} for i in data]


def test_get_groups_with_max_students(app):
    expected_data = db.session.query(GroupModel).all()
    repo = GroupRepository(db.session)
    test_input = repo.get_groups_with_max_students(23)
    db.session.close()
    assert valid_format_of_data(test_input) == valid_format_of_data(expected_data)
