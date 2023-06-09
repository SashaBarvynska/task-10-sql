from src.database.models import StudentModel


def test_post(client, session):
    response = client.post(
        "/students", json={"first_name": "Bob", "last_name": "Bondarenko"}
    )
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "id": 1, "first_name": "Bob", "last_name": "Bondarenko"}'
    )


def test_get(client, session):
    response = client.get("/students")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'[{"id":2,"first_name":"John","last_name":"Doe"}]'
    )


def test_get(client, session):
    response = client.get("/students/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'{"id":2,"first_name":"John","last_name":"Doe"}'
    )


def test_delete(client, session):
    response = client.delete("/students/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "message": "Student by 2 has been deleted."}'
    )


def test_delete_error(client, session):
    response = client.delete("/students/8")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "error": "Student by 8 not found."}'
    )


def test_patch(client, session):
    response = client.patch("/students/2", json={"last_name": "Bondarenko"})
    expected_data = session.query(StudentModel).filter(StudentModel.id == 2).first()
    assert response.status_code == 200
    assert expected_data.last_name == "Bondarenko"
