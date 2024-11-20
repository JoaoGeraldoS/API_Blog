from flask import Blueprint, request, jsonify
from app.models import Comments, db, Users
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, fields, Resource
from app.serializer import CommentsSchema

rota_comment = Blueprint('comments', __name__)
api = Namespace('Comments', description='Operação do comentario')

comment_model = api.model('Comment', {
    'content': fields.String(required = True, description = 'Conteudo do comentario'),
    'post_id': fields.Integer(required = True, description = 'Id do comentario'),
})

@api.route('/')
class CommentsDocumentation(Resource):
    @api.doc('create_comment')
    @api.expect(comment_model)
    @jwt_required()
    def post(self):
        """Cria comentario"""
        current_user = get_jwt_identity()

        user = Users.query.filter_by(username = current_user).first()

        content = request.json['content']
        post_id = request.json['post_id']
        

        comment = Comments(content = content, post_id = post_id, user_id = user.id)
        db.session.add(comment)
        db.session.commit()

        response = jsonify({'message': 'Comentario criado'})
        response.status_code = 201
        return response

    @api.doc('read_comments')
    def get(self):
        """Mostra os comentarios"""
        comment = Comments.query.all()

        user_schema = CommentsSchema(many = True)
        response = user_schema.jsonify(comment)
        response.status_code = 200
        return response


@api.route('/<int:id>')
class DeleteComments(Resource):
    @api.doc('delete_comment')
    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        comment = Comments.query.filter_by(id = id).first()
        user = Users.query.filter_by(username = current_user).first()

        if not comment:
            return jsonify({'message': 'Não existe esse comentario'})
        
        if comment.user_id == user.id:
            db.session.delete(comment)
            db.session.commit()

            response = jsonify({'message': 'comentario apagado'})
            response.status_code = 200
            return response
        
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response



