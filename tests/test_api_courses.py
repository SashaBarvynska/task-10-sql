def test_delete_student(client, session):
    response = client.delete("/courses/2/students/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "message": "Course by id 2 has been deleted."}'
    )


def test_delete_student_error(client, session):
    response = client.delete("/courses/10/students/2")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "error": "Course by id 10 not found."}'
    )


def test_get(client, session):
    response = client.get("/courses/2/students")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'[{"id":2,"first_name":"John","last_name":"Doe"}]'
    )


def test_post(client, session):
    response = client.post("/courses/3/students", json={"student_id": 2})
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "message": "Course was added successfully."}'
    )


def test_post_error(client, session):
    response = client.post("/courses/2/students", json={"student_id": 2})
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "error": "This course by id  2 already exists."}'
    )


def test_get(client, session):
    response = client.get("/courses")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'[{"id":2,"name":"Biology","description":null},{"id":3,"name":"Math","description":null}]'
    )


def test_post(client, session):
    response = client.post("/courses", json={"name": "Nails"})
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "message": "Course was created successfully."}'
    )


def test_get(client, session):
    response = client.get("/courses/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'{"id":2,"name":"Biology","description":null}'
    )


def test_delete(client, session):
    response = client.delete("/courses/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "message": "Course by 2 has been deleted."}'
    )


def test_delete_error(client, session):
    response = client.delete("/courses/1")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "error": "Course by 1 not found."}'
    )
