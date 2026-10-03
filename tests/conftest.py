import pytest
from urllib.parse import quote_plus

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.main import app
from app.config import settings
from app.database import get_db
from app.oauth2 import create_access_token

# Safely encode special characters in the password
encoded_password = quote_plus(settings.database_password)
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{encoded_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
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
    user_data = {"email": "testtuser@gmail.com", "password": "pass1234"}
    res = client.post("/users/", json = user_data)
    new_user = res.json()
    assert res.status_code == 201
    new_user["password"] = user_data.get("password")
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "newuser@gmail.com", "password": "pass1234"}
    res = client.post("/users/", json = user_data)
    new_user = res.json()
    assert res.status_code == 201
    new_user["password"] = user_data.get("password")
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [
        {
            "title": "Title 1",
            "content": "Content 1",
            "user_id": test_user["id"]
        },
        {
            "title": "Title 2",
            "content": "Content 2",
            "user_id": test_user["id"]
        },
        {
            "title": "Title 3",
            "content": "Content 3",
            "user_id": test_user["id"]
        },
        {
            "title": "Title 4",
            "content": "Content 4",
            "user_id": test_user2["id"]
        }
    ]
    def create_post_objects(post):
        return models.Post(**post)

    post_map = map(create_post_objects, post_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
