from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post: dict):
        return schemas.PostOut(**post)

    list(map(validate, res.json()))
    """
    By converting the result of map to a list like above code,
    you ensure that the validate function is actually called for each post in the response.
    The map function alone creates an iterator, which won't execute until it's consumed.
    Converting it to a list forces the execution.
    or we can simply use the below list comprehension

    [schemas.PostOut(**post) for post in res.json()]
    """

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    # test_posts is pytest fixture & will call test_user
    # for creating user. so we do not need to pass it in function's
    # parameters as an argument.

    res = client.get("/posts/")

    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get("/posts/999")
    # res = authorized_client.get(f"/posts/{test_posts[999].id}")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())  # validating by pydantic model

    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

    assert res.status_code == 200


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("favorite pizza", "i love pepperoni", False),
        ("tallest skyscrapers", "wahoo", False),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/", json={"title": "bla bla title", "content": "bla bla content"}
    )
    post = res.json()

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "bla bla title"
    assert created_post.content == "bla bla content"
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]


def test_authorized_user_create_post(client, test_user, test_posts):
    # test_user and test_posts is clearly unnecessary but just
    # for having a user and at least 3 posts in database before
    # the test run.
    res = client.post(
        "/posts/", json={"title": "bla bla title", "content": "bla bla content"}
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_exists(authorized_client, test_posts):
    res = authorized_client.delete("/posts/999")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {"title": "UPDATED title", "content": "UPDATED content", "published": False}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_posts):
    data = {"title": "UPDATED title", "content": "UPDATED content", "published": False}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_update_post_not_exists(authorized_client, test_posts):
    data = {"title": "UPDATED title", "content": "UPDATED content", "published": False}
    res = authorized_client.put("/posts/999", json=data)
    assert res.status_code == 404
