def test_get(client, session):
    response = client.get("/groups")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'[{"id":2,"name":"AA"},{"id":3,"name":"BB"}]'
    )


def test_post(client, session):
    response = client.post("/groups", json={"name": "Nails"})
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "id": 1, "name": "Nails"}'
    )


def test_delete(client, session):
    response = client.delete("/groups/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "message": "Group with id 2 has been deleted."}'
    )


def test_delete_error(client, session):
    response = client.delete("/groups/1")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{ "error": "Group with id 1 not found."}'
    )


def test_get(client, session):
    response = client.get("/groups/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'{"id":2,"name":"AA"}'
    )
