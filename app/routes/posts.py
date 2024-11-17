from flask import Blueprint, jsonify, request
from app.models import db, Posts

api = Blueprint('api', __name__)

@api.route('/posts', methods=['POST'])
def criar_tarefa():
    title = request.json['title']
    content = request.json['content']
    author_id = request.json['author_id']

    post = Posts(title = title, content = content, author_id = author_id)

    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'post criado'}), 201

@api.route('/tarefas/', methods=['GET'])
def listar_tarefas():
    tarefas = Posts.query.all()
    return jsonify([{"id": t.id, "nome": t.nome} for t in tarefas])
