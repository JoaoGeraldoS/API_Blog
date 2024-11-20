from app.models import db, Posts

"""Teste para criar tags"""
def test_add_tag(client, auth_headers):
    response = client.post('/tags/', json = {
        'name': ['Tag 1', 'Tag 2']
    }, headers = auth_headers)

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'tag registrada'



"""Teste para associar tag ao post"""
def test_add_tag_post(client, auth_headers):
    post = Posts(title="Test Post", content="Content for testing")
    db.session.add(post)
    db.session.commit()

    respose = client.put('/tags/post/1', json = {
        'tag_id': 1
    }, headers = auth_headers)

    assert respose.status_code == 201
    data = respose.get_json()
    assert data['message'] == 'tag adiciona'


"""Teste para listar todas as tags"""
def test_read_tag(client):
    response_read = client.get('/tags/')
    
    assert response_read.status_code == 200

    tags = response_read.get_json()

    assert len(tags) >= 1
    tag = tags[0]
    assert tag['name'] == 'Tag 1'


"""Teste para listar uma tag especifica"""
def test_read_specific_tag(client):
    response = client.get('/tags/1')
    assert response.status_code == 200

    data = response.get_json()
    assert data['name'] == 'Tag 1'


"""Teste para autualizar tag"""
def test_update_tag(client, auth_headers):
    response = client.put('/tags/1',json = {
        'name': 'Tag 3'
    }, headers = auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'tag atualizada'

"""Teste para apagar uma tag"""
def test_delete_tag(client, auth_headers):
    response = client.delete('/tags/1', headers = auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'tag apagada'