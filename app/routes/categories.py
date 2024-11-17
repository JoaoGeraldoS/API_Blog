from flask import Blueprint, request, jsonify
from app.models import Categories, PostCategory, db, Posts

rota_category = Blueprint('categories', __name__)

@rota_category.route('/categories', methods = ['POST'])
def create_category():
    name = request.json['name']

    for category in name:
        add_category = Categories(name = category)
        db.session.add(add_category)
        db.session.commit()
    
    return jsonify({'message': 'Categoria registrada'}), 201




@rota_category.route('/category/post/<int:id>', methods = ['PUT'])
def add_category_post(id):
    post = Posts.query.filter_by(id = id).first()

    category_id = request.json['category_id']

    category_post = PostCategory(category_id = category_id, post_id = post.id)
    db.session.add(category_post)
    db.session.commit()

    return jsonify({'message': 'categoria adiciona'}), 201

        