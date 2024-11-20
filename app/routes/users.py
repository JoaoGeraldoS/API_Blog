from flask import Blueprint, jsonify, request
from app.models import db, Users
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from flask_restx import Namespace, fields, Resource
from app.serializer import UsersSchema

rota_user = Blueprint('users', __name__)
api = Namespace('Users', description='Operação do usuario')


user_model = api.model('User', {
    'name': fields.String(required = True, description='Nome do usuario'),
    'username': fields.String(required = True, description='username do usuario'),
    'email': fields.String(required = True, description='email do usuario'),
    'password': fields.String(required = True, description='senha do usuario'),
    'author': fields.Boolean(required = True, description='Verifica se o usuario é autor'),
})

login_model = api.model('Login', {
    'username': fields.String(required = True, description='username do usuario'),
    'password': fields.String(required = True, description='senha do usuario'),
})


@api.route('/')
class UsersDocumentation(Resource):
    @api.doc('create_user')
    @api.expect(user_model)
    
    def post(self):
        """Cria usuario"""
        name = request.json['name']
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        author = request.json['author']

        user = Users(name=name, username=username, email=email, password=password, author = author)
        db.session.add(user)
        db.session.commit()

        response = jsonify({'message': 'usuario criado'})
        response.status_code = 201
        return response
    
perfil_update = api.model('Perfil', {
    'name': fields.String(required = True, description='Nome do usuario'),
    'password': fields.String(required = True, description='senha do usuario'),
    'author': fields.Boolean(required = True, description='Verifica se o usuario é autor'),
})



@api.route('/<int:id>')
class PerfilUser(Resource):
    @api.doc('update_perfil')
    @api.expect(perfil_update)
    @jwt_required()
    def put(self, id):
        """Atualiza perfil do usuario"""
        current_user = get_jwt_identity()

        user = Users.query.filter_by(id = id).first()

        user.name = request.json['name']
        user.password = request.json['password']
        user.author = request.json['author']

        db.session.commit()

        response = jsonify({'message': 'Perfil atualizado'})
        response.status_code = 200
        return response
    
    @api.doc('read_perfil')
    def get(self, id):
        """Mostra Perfil do usuario"""
        user = Users.query.filter_by(id = id).first()

        if not user:
            return jsonify({'message': 'Usuario não existe'}), 404
        
        user_schema = UsersSchema()
        response = user_schema.jsonify(user)
        response.status_code = 200
        return response
    



@api.route('/login')
class LoginDocuments(Resource):
    @api.doc('login')
    @api.expect(login_model)
    def post(self):
        """Login do usuario"""
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
