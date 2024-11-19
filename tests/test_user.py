def test_create_user(client):
    response = client.post('/users', json={
        'name': 'Joao',
        'username': 'testuser',
        'email': 'teste@test.com',
        'password': 'testpassword',
        'author': True
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'usuario criado'


def test_login(client):
    response = client.post('/login', json = {
        'username': 'testuser',
        'password': 'testpassword'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login realizado'