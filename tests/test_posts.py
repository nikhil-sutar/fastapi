import pytest
from app import schemas

def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_post(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_user_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/7999")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("Favourite Pizaa", "I love farm house pizza", False),
    ("Top beaches in Goa", "Beaches in goa are awesome", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.user_id == test_user["id"]

def test_create_post_deafult_published(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "Some Title", "content": "Some Content"})
    post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert post.title == "Some Title"
    assert post.content == "Some Content"
    assert post.published == True
    assert post.user_id == test_user["id"]

def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={"title": "Some Title", "content": "Some Content"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_posts):
    res = authorized_client.delete("/posts/7777")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data["content"]

def test_other_user_update_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_non_exist_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put("/posts/7777", json=data)
    assert res.status_code == 404