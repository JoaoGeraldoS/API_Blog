def test_comment(client, auth_headers):
    respose = client.post('/comments/', json = {
        'content': 'Conteudo do comentario',
        'post_id': 1,
        
    }, headers = auth_headers)

    assert respose.status_code == 201
    data = respose.get_json()
    assert data['message'] == 'Comentario criado'


def test_read_comments(client):
    response = client.get('/comments/')

    assert response.status_code == 200
    data = response.get_json()

    assert len(data) == 1
    comment = data[0]
    assert comment['content'] == 'Conteudo do comentario'


def test_delete_comment(client, auth_headers):
    response = client.delete('/comments/1', headers = auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'comentario apagado'