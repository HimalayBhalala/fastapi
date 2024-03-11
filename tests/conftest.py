from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from app import oauth
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("My session run")
    Base.metadata.drop_all(bind=engine)   
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    # command.upgrade('head')
    # command.downgrade('base')
    
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)    
    
    
@pytest.fixture
def test_user(client):
    user_data = {"email":"hello@gmail.com",
                 "password":"123"}
    res = client.post('/users/',json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(client,test_user):
    return oauth.create_access_token({'user_id':test_user['id']})

@pytest.fixture
def client_authenticate(client,token):
    client.headers = {
        **client.headers,
        'Authorization' : f"Bearer {token}"
    }
    print(token)
    return client 

@pytest.fixture
def test_posts(test_user,session):
    posts_data = [{
        "title":"first",
        "content":"first",
        "owner_id":test_user['id']
    },
    {
        "title":"second",
        "content":"second",
        "owner_id":test_user['id']
    },
    ]
    
    # session.add_all([models.Post(title="first",context = "first",owner_id=test_user['id'])])
    
    def create_user_model(post):
        return models.Post(**post)
    
    posts_map =  map(create_user_model,posts_data)
    
    posts = list(posts_map)
    print(posts)
    session.add_all(posts)
    
    session.commit()
    
    post_data = session.query(models.Post).all()
    
    return post_data