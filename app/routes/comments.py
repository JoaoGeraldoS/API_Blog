from flask import Blueprint, request, jsonify
from app.models import Comments, db

rota_comment = Blueprint('comments', __name__)

@rota_comment.route('/comments', methods = ['POST'])
def create_comment():
    content = request.json['content']
    post_id = request.json['post_id']
    user_id = request.json['user_id']

    comment = Comments(content = content, post_id = post_id, user_id = user_id)
    db.session.add(comment)
    db.session.commit()

    return jsonify({'message': 'Comentario criado'}), 201

