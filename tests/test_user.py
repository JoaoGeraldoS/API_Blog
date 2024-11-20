def test_create_user(client):
    response = client.post('/users/', json={
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
    response = client.post('/users/login', json = {
        'username': 'testuser',
        'password': 'testpassword'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login realizado'

def test_read_perfil_user(client):
    response = client.get('/users/1')

    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Joao' 

def test_update_perfil_user(client, auth_headers):
    response = client.put('/users/1', json = {
        'name': 'testuser',
        'password': 'testpassword',
        'author': True
    }, headers = auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Perfil atualizado'
