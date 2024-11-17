from app.models import db, Posts

def test_add_category(client):
    response = client.post('/categories', json = {
        'name': ['Categoria 1', 'Categoria 2']
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Categoria registrada'

def test_add_category_post(client):

    post = Posts(title="Test Post", content="Content for testing")
    db.session.add(post)
    db.session.commit()

    respose = client.put('/category/post/1', json = {
        'category_id': 1
    })

    assert respose.status_code == 201
    data = respose.get_json()
    assert data['message'] == 'categoria adiciona'