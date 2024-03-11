import pytest
from app import schemas
from .database import client,session
from app import schemas
# from .conftest import test_user
from jose import jwt
from app.config import settings

# def test_hello(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == "Hello World"
#     assert res.status_code == 200
    
# def test_create_user(client):
#     res = client.post('/users/',json={"email":"hello@gmail.com","password":"123"})
#     user = schemas.UserOut(**res.json())
#     assert user.email == "hello@gmail.com"
#     assert res.status_code == 201
    
    
def test_login_user(client,test_user):
    res = client.post('/login',data={"username":test_user['email'],"password":test_user['password']})
    token_info = schemas.Token(**res.json())
    payload = jwt.decode(token_info.access_token,settings.secret_key,settings.algorithm)
    id = payload.get('user_id')
    assert id == test_user['id']
    assert token_info.token_type == 'bearer'
    assert res.status_code == 200
    

@pytest.mark.parametrize("email,password,status_code",[
    ('wrong@gmail.com','123',403),
    ('hello@gmail.com','wrong_password',403),
    ('wrong@gmail.com','wrong_password',403),
    (None,'wrong_password',422),
    ('hello@gmail.com',None,422),
])
def test_incorrect_login(test_user,client,email,password,status_code):
    res = client.post('/login',data={'username':email,'password':password})
    assert res.status_code == status_code