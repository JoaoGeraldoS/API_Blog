from app.models import db, Posts

"""Teste para criar categoria"""
def test_add_category(client, auth_headers):
    response = client.post('/categories/', json = {
        'name': ['Categoria 1', 'Categoria 2']
    }, headers = auth_headers)

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Categoria registrada'


"""Teste para associar categoria ao post"""
def test_add_category_post(client, auth_headers):
    post = Posts(title="Test Post", content="Content for testing")
    db.session.add(post)
    db.session.commit()

    respose = client.put('/categories/post/1', json = {
        'category_id': 1
    }, headers = auth_headers)

    assert respose.status_code == 201
    data = respose.get_json()
    assert data['message'] == 'Categoria adiciona'


"""Teste para listar todas as categorias"""
def test_read_category(client):
    response_read = client.get('/categories/')
    
    assert response_read.status_code == 200

    categories = response_read.get_json()

    assert len(categories) >= 1
    category = categories[0]
    assert category['name'] == 'Categoria 1'


"""Teste para listar uma categoria especifica"""
def test_read_specific_category(client):
    response = client.get('/categories/1')
    assert response.status_code == 200

    data = response.get_json()
    assert data['name'] == 'Categoria 1'


"""Teste para autualizar categoria"""
def test_update_category(client, auth_headers):
    response = client.put('/categories/1',json = {
        'name': 'Categoria 2'
    }, headers = auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'categoria atualizada'

"""Teste para apagar uma categoria"""
def test_delete_category(client, auth_headers):
    response = client.delete('/categories/1', headers = auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'categoria apagada'