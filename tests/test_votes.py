import pytest
from app import models


@pytest.fixture
def test_vote(test_user, test_posts, session):
    new_vote = models.Vote(user_id=test_user["id"], post_id=test_posts[3].id)
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    data = {"post_id": test_posts[3].id, "dir": 1}
    res = authorized_client.post(f"/vote/", json=data)
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    data = {"post_id": test_posts[3].id, "dir": 1}
    res = authorized_client.post(f"/vote/", json=data)
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    data = {"post_id": test_posts[3].id, "dir": 0}
    res = authorized_client.post(f"/vote/", json=data)
    assert res.status_code == 201


def test_delete_vote_not_exists(authorized_client, test_posts):
    data = {"post_id": test_posts[3].id, "dir": 0}
    res = authorized_client.post(f"/vote/", json=data)
    assert res.status_code == 404


def test_vote_post_not_exists(authorized_client, test_posts):
    data = {"post_id": 999, "dir": 1}
    res = authorized_client.post(f"/vote/", json=data)
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_vote, test_posts):
    data = {"post_id": test_posts[3].id, "dir": 1}
    res = client.post(f"/vote/", json=data)
    assert res.status_code == 401
