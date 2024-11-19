from flask import Blueprint, jsonify, request
from app.models import db, Users
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

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


@rota_user.route('/login', methods = ['POST'])
def login():
    username = request.json['username']
    passowrd = request.json['password']

    user = Users.query.filter_by(username = username).first()

    if user.username != username or user.password != passowrd:
        return jsonify({'message': 'username ou senha invalidos!'})

    if user.author:
        token_author = create_access_token(identity=username, expires_delta=timedelta(hours=2))
        return jsonify({'message': 'Login realizado', 'token': token_author})
    else:
        token_user = create_access_token(identity=username, expires_delta=timedelta(hours=2))
        return jsonify({'message': 'Login realizado', 'token': token_user})
    