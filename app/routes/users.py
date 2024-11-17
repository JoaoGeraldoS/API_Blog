from flask import Blueprint, jsonify, request
from app.models import db, Users

rota_user = Blueprint('users', __name__)

@rota_user.route('/users', methods=['POST'])
def create_users():

    name = request.json['name']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    author = request.json['author']

    user = Users(name=name, username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'usuario criado'}), 201
