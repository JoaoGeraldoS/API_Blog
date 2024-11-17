import json

def test_criar_tarefa(client):
    """Teste de criação de tarefa"""
    response = client.post('/posts', json={
        'title': 'A menina e o porquinho',
        'content': 'Teste',
        'author_id': 1
    })

    
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == "post criado"

# def test_listar_tarefas(client):
#     """Teste de listagem de tarefas"""
#     client.post('/tarefas/', json={"nome": "Estudar Flask"})
#     client.post('/tarefas/', json={"nome": "Aprender Pytest"})
    
#     response = client.get('/tarefas/')
#     assert response.status_code == 200
#     data = response.get_json()
#     assert len(data) == 2
#     assert data[0]['nome'] == "Estudar Flask"
#     assert data[1]['nome'] == "Aprender Pytest"
