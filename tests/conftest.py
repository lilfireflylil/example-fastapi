# conftest.py has special meaning in pytest.
# fixtures that you will define will be shared among all tests in your test suite.
# so you won't need to import them in every file.

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "email@email.com", "password": "password123"}
    res = client.post(
        "/users/", json=user_data
    )  # creating temporary user in testing database

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "email2@email2.com", "password": "password123"}
    res = client.post(
        "/users/", json=user_data
    )  # creating temporary user in testing database

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_posts(session, test_user, test_user2):
    post_data = [
        {"title": "1st title", "content": "1st", "user_id": test_user["id"]},
        {"title": "2nd title", "content": "2nd", "user_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd", "user_id": test_user["id"]},
        {
            "title": "4rd title by test_user2",
            "content": "4rd",
            "user_id": test_user2["id"],
        },
    ]

    def create_post_model(post: dict):
        return models.Post(**post)

    posts = list(map(create_post_model, post_data))
    # posts = [models.Post(**post) for post in post_data]

    session.add_all(posts)

    # session.add_all(
    #     [
    #         models.Post(title="1st title", content="1st", user_id=test_user["id"]),
    #         models.Post(title="2nd title", content="2nd", user_id=test_user["id"]),
    #         models.Post(title="3rd title", content="3rd", user_id=test_user["id"]),
    #     ]
    # )

    session.commit()

    posts = session.query(models.Post).all()
    return posts
