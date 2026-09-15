from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_register_and_login():
    r = client.post("/register", json={
        "username": "testuser_pytest",
        "password": "123456"
    })
    assert r.status_code in (200, 400)

    r = client.post("/login", json={
        "username": "testuser_pytest",
        "password": "123456"
    })
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password():
    r = client.post("/login", json={
        "username": "testuser_pytest",
        "password": "wrongpassword"
    })
    assert r.status_code == 401
def get_token(username, password):
    r = client.post("/login", json={"username": username, "password": password})
    return r.json()["access_token"]


def test_todos_require_login():
    r = client.get("/todos")
    assert r.status_code == 401


def test_todo_crud_flow():
    client.post("/register", json={"username": "pytest_crud", "password": "123456"})
    token = get_token("pytest_crud", "123456")
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post("/todos", json={"text": "写测试"}, headers=headers)
    assert r.status_code == 200
    todo_id = r.json()["id"]

    r = client.get("/todos", headers=headers)
    texts = [t["text"] for t in r.json()]
    assert "写测试" in texts

    r = client.patch(f"/todos/{todo_id}", headers=headers)
    assert r.status_code == 200

    r = client.get("/todos", headers=headers)
    target = [t for t in r.json() if t["id"] == todo_id][0]
    assert target["done"] is True

    r = client.delete(f"/todos/{todo_id}", headers=headers)
    assert r.status_code == 200

    r = client.get("/todos", headers=headers)
    ids = [t["id"] for t in r.json()]
    assert todo_id not in ids


def test_user_isolation():
    client.post("/register", json={"username": "pytest_a", "password": "123456"})
    client.post("/register", json={"username": "pytest_b", "password": "123456"})

    token_a = get_token("pytest_a", "123456")
    token_b = get_token("pytest_b", "123456")
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    r = client.post("/todos", json={"text": "A 的隐私"}, headers=headers_a)
    a_todo_id = r.json()["id"]

    r = client.get("/todos", headers=headers_b)
    b_ids = [t["id"] for t in r.json()]
    assert a_todo_id not in b_ids

    r = client.delete(f"/todos/{a_todo_id}", headers=headers_b)
    assert r.status_code == 404

    client.delete(f"/todos/{a_todo_id}", headers=headers_a)