def test_cria_users(client):
    response = client.post('/users', json={
        'name': 'Joao',
        'username': 'joao',
        'email': 'email@email.com',
        'password': 'senha',
        'author': True
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'usuario criado'