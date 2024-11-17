from app.models import db, Posts

def test_add_tag(client):
    response = client.post('/tags', json = {
        'name': ['Tag 1', 'Tag 2']
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Tag registrada'

def test_add_tag_post(client):

    post = Posts(title="Test Post", content="Content for testing")
    db.session.add(post)
    db.session.commit()

    respose = client.put('/tag/post/1', json = {
        'tag_id': 1
    })

    assert respose.status_code == 201
    data = respose.get_json()
    assert data['message'] == 'tag adiciona'