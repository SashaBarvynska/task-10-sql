from src.database.models import StudentModel


def test_post_create_new_student(client, session):
    response = client.post(
        "/students", json={"first_name": "Bob", "last_name": "Bondarenko"}
    )
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'{"first_name":"Bob","id":1,"last_name":"Bondarenko"}'
    )


def test_get_all_students(client, session):
    response = client.get("/students")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'[{"first_name":"John","id":2,"last_name":"Doe"}]'
    )


def test_get_student_by_id(client, session):
    response = client.get("/students/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'{"first_name":"John","id":2,"last_name":"Doe"}'
    )


def test_get_student_by_id_error(client, session):
    response = client.get("/students/33")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "error": "Student by 33 not found."}'
    )


def test_delete_student_by_id(client, session):
    response = client.delete("/students/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "message": "Student by 2 has been deleted."}'
    )


def test_delete_student_by_id_error(client, session):
    response = client.delete("/students/66")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "error": "Student by 66 not found."}'
    )


def test_patch(client, session):
    response = client.patch(
        "/students/2", json={"last_name": "Bondarenko", "first_name": "Sara"}
    )
    expected_data = session.query(StudentModel).filter(StudentModel.id == 2).first()
    assert response.status_code == 200
    assert expected_data.last_name == "Bondarenko"
