import pytest
from app import schemas
from jose import jwt
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))
#     assert res.json().get("message") == "hello World"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "email@email.com", "password": "password123"}
    )
    # We need to add trailing slash in url because in users.py we have
    # prefix="/users" and then for "create_user" function url is trailing slash
    # for example: "/users/" instead of "/users"

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "email@email.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])

    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("WrongEmail@email.com", "password123", 403),
        ("email@email.com", "WrongPassword", 403),
        (None, "password123", 422),
        ("email@email.com", None, 422),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password}
    )

    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid credentials"
