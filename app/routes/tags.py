from flask import Blueprint, request, jsonify
from app.models import Tags, PostTags, db, Posts

rota_tag = Blueprint('tags', __name__)

@rota_tag.route('/tags', methods = ['POST'])
def create_tag():
    name = request.json['name']

    for tag in name:
        add_tag = Tags(name = tag)
        db.session.add(add_tag)
        db.session.commit()
    
    return jsonify({'message': 'Tag registrada'}), 201




@rota_tag.route('/tag/post/<int:id>', methods = ['PUT'])
def add_tag_post(id):
    post = Posts.query.filter_by(id = id).first()

    tag_id = request.json['tag_id']

    tag_post = PostTags(tag_id = tag_id, post_id = post.id)
    db.session.add(tag_post)
    db.session.commit()

    return jsonify({'message': 'tag adiciona'}), 201