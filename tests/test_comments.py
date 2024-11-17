def test_comment(client):
    respose = client.post('/comments', json = {
        'content': 'Conteudo do comentario',
        'post_id': 1,
        'user_id': 1
    })

    assert respose.status_code == 201
    data = respose.get_json()
    assert data['message'] == 'Comentario criado'