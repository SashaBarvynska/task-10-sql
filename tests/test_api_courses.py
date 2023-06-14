def test_delete_course_student(client, session):
    response = client.delete("/courses/2/students/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n  ", b"").replace(b"\n", b"")
        == b'{"message": "Course by id 2 has been deleted from student with id 2."}'
    )


def test_delete_course_student_error(client, session):
    response = client.delete("/courses/10/students/2")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n  ", b"").replace(b"\n", b"")
        == b'{"error": "Student with id 2 is not assigned to course with id 10"}'
    )


def test_get_all_students_to_course(client, session):
    response = client.get("/courses/2/students")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'[{"first_name":"John","id":2,"last_name":"Doe"}]'
    )


def test_get_course_not_found_error(client, session):
    response = client.get("/courses/90/students")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n  ", b"").replace(b"\n", b"")
        == b'{"error": "Course by id 90 not found."}'
    )


def test_post_add_course_to_student(client, session):
    response = client.post("/courses/3/students", json={"student_id": 2})
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n", b"")
        .replace(b"\n  ", b"")
        .replace(b"\\u0421", b"C")
        == b'{  "message": "Course has been successfully added"}'
    )


def test_post_course_student_exist_error(client, session):
    response = client.post("/courses/2/students", json={"student_id": 2})
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "error": "Student with id 2 is already assigned to course with id 2."}'
    )


def test_post_student_not_exist_error(client, session):
    response = client.post("/courses/2/students", json={"student_id": 90})
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "error": "This student by id  90 is not exists."}'
    )


def test_post_course_not_found_error(client, session):
    response = client.post("/courses/67/students", json={"student_id": 3})
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "error": "Course by id 67 not found."}'
    )


def test_get_all_courses(client, session):
    response = client.get("/courses")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'[{"description":null,"id":2,"name":"Biology"},{"description":null,"id":3,"name":"Math"}]'
    )


def test_post_new_course(client, session):
    response = client.post("/courses", json={"name": "Nails"})
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "message": "Course with name Nails was created successfully."}'
    )


def test_get_course_id(client, session):
    response = client.get("/courses/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'{"description":null,"id":2,"name":"Biology"}'
    )


def test_get_course_id_error(client, session):
    response = client.get("/courses/67")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "error": "Course with 67 not found."}'
    )


def test_delete_course_id(client, session):
    response = client.delete("/courses/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "message": "Course by 2 has been deleted."}'
    )


def test_delete_course_id_error(client, session):
    response = client.delete("/courses/67")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "error": "Course by 67 not found."}'
    )
