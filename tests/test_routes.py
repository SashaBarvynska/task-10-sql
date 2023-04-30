import json

import pytest
from flask import Response


test_student = b'{"first_name": "Michael","id": 233,"last_name": "Bondarenko"}'


def test_add_student(client):
    response = client.post(
            '/students',
            data=json.dumps(dict(
                first_name='Michael',
                last_name='Bondarenko'
            )),
            content_type='application/json',
        )
    assert response.status_code == 200
    assert test_student == response.data.replace(b'\n  ', b'').replace(b'\n', b'')


@pytest.mark.parametrize("id, result",  [
    (11, b'{"message": "Student by 11 has been deleted."}'),
    (12, b'{"message": "Student by 12 has been deleted."}'),
    ])
def test_delete_student_successfully(id, result, client):
    response = client.delete(f'/students/{id}')
    assert response.status_code == 200
    assert result == response.data.replace(b'\n  ', b'').replace(b'\n', b'')


@pytest.mark.parametrize("id, result",  [
    (1, b'{"error": "Student by 1 not found."}'),
    (3, b'{"error": "Student by 3 not found."}'),
    ])
def test_delete_student_error(id, result, client):
    response = client.delete(f'/students/{id}')
    assert response.status_code == 404
    assert result == response.data.replace(b'\n  ', b'').replace(b'\n', b'')


@pytest.mark.parametrize("course, result",  [
    ("Biology", b'[{"first_name": "Russell", "id": 180, "last_name": "Howe"}]'),
    ("History", b'[{"id": 177, "first_name": "Daniel", "last_name": "Osborn"}]'),
    ])
def test_get_courses(course, result, client):
    response: Response = client.get(f"/students?course={course}")
    assert response.status_code == 200
    assert result == response.content_encoding


def test_handle_exception(client):
    response: Response = client.get("/students/&^%SashaBarvynska474")
    print("response: ", type(response.data), response.data.rstrip(), response.data.strip())
    assert response.status_code == 404
    assert response.data.replace(b'\n  ', b'').replace(b'\n', b'') == b'{"message": "Page Not Found"}'
