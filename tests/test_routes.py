import json
from flask import Response
import pytest
from src import StudentModel

test_student = b'{"first_name": "Sasha","id": 1,"last_name": "Barvynska"}'


def test_add_student(client, session):
    response = client.post(
        "/students",
        data=json.dumps(dict(first_name="Sasha", last_name="Barvynska")),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.data.replace(b"\n  ", b"").replace(b"\n", b"") == test_student


def test_delete_student_successfully(client, session):
    response = client.delete("/students/2")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "id, result",
    [
        (5, b'{"error": "Student by 5 not found."}'),
        (3, b'{"error": "Student by 3 not found."}'),
    ],
)
def test_delete_student_error(id, result, client, session):
    response = client.delete(f"/students/{id}")
    assert response.status_code == 404
    assert result == response.data.replace(b"\n  ", b"").replace(b"\n", b"")


def test_get_courses(client, session):
    response: Response = client.get("/students?course=Biology")
    assert response.status_code == 200
    assert response.data == b'[{"id": 2, "first_name": "John", "last_name": "Doe"}]'


def test_add_student_to_course_error(client, session):
    response: Response = client.post(
        "/students/add_course",
        data=json.dumps(dict(student_id=2, course_id=[1])),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert (
        response.data == b'{\n  "error": "This course by id [1] already exists."\n}\n'
    )


def test_add_student_to_course(client, session):
    response: Response = client.post(
        "/students/add_course",
        data=json.dumps(dict(student_id=2, course_id=[2])),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.data == b'{\n  "message": "Course was added successfully."\n}\n'


def test_delete_course_error(client, session):
    response: Response = client.delete("/students/2/courses?course=2")
    assert response.status_code == 404
    assert response.data == b'{\n  "error": "Course by id 2 not found."\n}\n'


def test_delete_course(client, session):
    response: Response = client.delete("/students/2/courses?course=1")
    assert response.status_code == 200
    assert response.data == b'{\n  "message": "Course by id 1 has been deleted."\n}\n'


def test_get_groups(client, session):
    response: Response = client.get("/groups?max_students=2")
    assert response.status_code == 200
    assert response.data == b'[{"id": 1, "name": "AA"}]'
