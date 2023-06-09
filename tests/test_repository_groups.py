from src.database.repositories.groups import GroupRepository
from src.database.models import GroupModel


def test_get_groups(app, session):
    repo = GroupRepository(session)
    result = repo.get_groups()
    expected_data = session.query(GroupModel).all()
    assert result == expected_data


def test_get_groups_max_student(app, session):
    repo = GroupRepository(session)
    result = repo.get_groups(4)
    expected_data = [session.query(GroupModel).first()]
    assert result == expected_data


def test_create_group(app, session):
    repo = GroupRepository(session)
    result = repo.create_group("Group_1")
    expected_data = (
        session.query(GroupModel).filter(GroupModel.name == result.name).first()
    )
    assert result == expected_data


def test_get_group_by_id(app, session):
    repo = GroupRepository(session)
    result = repo.get_group_by_id(2)
    expected_data = session.query(GroupModel).filter(GroupModel.id == result.id).first()
    assert result == expected_data


def test_delete_group_by_id(app, session):
    repo = GroupRepository(session)
    result = repo.delete_group_by_id(3)
    expected_data = session.query(GroupModel).filter(GroupModel.id == 3).first()
    assert result is expected_data
