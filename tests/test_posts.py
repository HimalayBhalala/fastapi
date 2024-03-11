def test_get_all_posts(client,client_authenticate):
    res = client.get('/posts/')
    assert res.status_code == 200  
 