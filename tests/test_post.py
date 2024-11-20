from .conftest import auth_headers
from app.models import Tags, Posts, db, Categories, PostCategory, PostTags, Users
"""Teste de criação de Posts"""
def test_create_post(client, auth_headers):
    response_category = client.post('/categories/', json = {
        'name': ['Categoria 1', 'Categoria 2']
    }, headers = auth_headers)

    assert response_category.status_code == 201

    response_tag = client.post('/tags/', json = {
        'name': ['Tag 1', 'Tag 2']
    }, headers = auth_headers)

    assert response_tag.status_code == 201

    post_data = {
        'title': 'A menina e o porquinho',
        'content': 'Teste',
        'author_id': 1,
        'categories': ['Categoria 1', 'Categoria 2', 'Categoria 3'],
        'tags': ['Tag 1', 'Tag 2', 'Tag 3']
    }

    response_post = client.post('/posts/' , json = post_data, headers = auth_headers)
   
    assert response_post.status_code == 201
    data = response_post.get_json()
    assert data['message'] == "post criado"


"""Teste de leitura dos posts"""
def test_read_post(client):
    response_read = client.get('/posts/')
    
    assert response_read.status_code == 200

    posts = response_read.get_json()

    assert len(posts) == 1
    post = posts[0]
    assert post['title'] == 'A menina e o porquinho'


"""Teste de leitura de um post especifico"""
def test_read_specific_post(client):
    response_read_id = client.get('/posts/1')

    assert response_read_id.status_code == 200

    post = response_read_id.get_json()
    assert post['title'] == 'A menina e o porquinho'


"""Teste de atualização de um post"""
def test_update_post(client, auth_headers):
    response = client.put('/posts/1', json = {
        'title': 'As tranças do rei careca',
        'content': 'Tiao galinha'
    }, headers = auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Post atualizado'


"""Teste para apagar um post """
def test_delete_post(client, auth_headers):
    response = client.delete('/posts/1', headers = auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Post deletado'


def test_filter_post_categroies(client, auth_headers):
    response_category = client.post('/categories/', json = {
        'name': ['Categoria 1', 'Categoria 2']
    }, headers = auth_headers)

    assert response_category.status_code == 201

    response_tag = client.post('/tags/', json = {
        'name': ['Tag 1', 'Tag 2']
    }, headers = auth_headers)

    assert response_tag.status_code == 201

    post_data = {
        'title': 'A menina e o porquinho',
        'content': 'Teste',
        'author_id': 1,
        'categories': ['Categoria 1', 'Categoria 2', 'Categoria 3'],
        'tags': ['Tag 1', 'Tag 2', 'Tag 3']
    }

    response_post = client.post('/posts/' , json = post_data, headers = auth_headers)
   
    assert response_post.status_code == 201
    data = response_post.get_json()
    assert data['message'] == "post criado"

    response = client.get('/posts/filter?category=Categoria 1')
    
    
    # Obter os dados do JSON retornado
    response_data = response.get_json()
    print('Resposta do teste:',response_data)

 
    
    
    

# def test_filter_post_tags(client):
#     tag = Tags(name='Tag 1')
#     db.session.add(tag)
#     db.session.commit()

#     post = Posts(title='Post Teste', content = 'Conteudo do post')
#     db.session.add(post)
#     db.session.commit()

#     post_tags = PostTags(post_id = post.id, tag_id = tag.id)
#     db.session.add(post_tags)
#     db.session.commit()

#     response = client.get('/posts/?tag=Tag 3')

#     # Validações
#     assert response.status_code == 200

#     # Obter os dados do JSON retornado
#     response_data = response.get_json()

#     assert len(response_data) > 0
#     assert response_data[0]['title'] == 'Post Teste'

