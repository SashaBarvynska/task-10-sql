def test_get_all_groups(client, session):
    response = client.get("/groups")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'[{"id":2,"name":"AA"},{"id":3,"name":"BB"}]'
    )


def test_post_create_new_group(client, session):
    response = client.post("/groups", json={"name_group": "Nails"})
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'{"id":1,"name":"Nails"}'
    )


def test_delete_group_by_id(client, session):
    response = client.delete("/groups/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "message": "Group with id 2 has been deleted."}'
    )


def test_delete_group_by_id_error(client, session):
    response = client.delete("/groups/1")
    assert response.status_code == 404
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"")
        == b'{  "error": "Group with id 1 not found."}'
    )


def test_get_group_by_id(client, session):
    response = client.get("/groups/2")
    assert response.status_code == 200
    assert (
        response.data.replace(b"\n   ", b"").replace(b"\n", b"").replace(b" ", b"")
        == b'{"id":2,"name":"AA"}'
    )
