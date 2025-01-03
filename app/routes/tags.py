from flask import Blueprint, request, jsonify
from app.models import Tags, PostTags, db, Posts, Users
from flask_restx import Namespace, fields, Resource
from app.serializer import TagsSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

rota_tag = Blueprint('tags', __name__)
api = Namespace('Tags', description='Operações das tags')


tag_model = api.model('Tag', {
    'name': fields.String(required = True, description = 'Nome da tag')
})


@api.route('/')
class TagDocumentation(Resource):
    @api.doc('create_tag')
    @api.expect(tag_model)
    @jwt_required()
    def post(self):
        """Cria tag"""
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:
            name = request.json['name']

            for tag in name:
                add_tag = Tags(name = tag)
                db.session.add(add_tag)
                db.session.commit()
            
            response = jsonify({'message': 'tag registrada'})
            response.status_code = 201
            return response
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response
    

    @api.doc('read_tag')
    def get(self):
        """Mostra tags"""
        tag = Tags.query.all()

        category_schema = TagsSchema(many = True)
        response = category_schema.jsonify(tag)
        response.status_code = 200
        return response


@api.route('/<int:id>')
class SpecificTag(Resource):
    @api.doc('update_tag')
    @api.expect(tag_model)
    @jwt_required()
    def put(self, id):
        """Atualiza tag"""
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:
            tag = Tags.query.filter_by(id = id).first()
            
            if not tag:
                return jsonify({'message': 'tag não encontrada'}), 404
            
            tag.name = request.json['name']
            db.session.commit()

            response = jsonify({'message': 'tag atualizada'})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response
    

    @api.doc('read_specific_tag')
    def get(self, id):
        """Mostra tag especifica"""
        tag = Tags.query.filter_by(id = id).first()

        if not tag:
            return jsonify({'message': 'tag não existe'}), 404
        
        tag_schema = TagsSchema()
        response = tag_schema.jsonify(tag)
        response.status_code = 200
        return response
    

    @api.doc('delete_tag')
    @jwt_required()
    def delete(self, id):
        """Apaga tag"""
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:
            tag = Tags.query.filter_by(id = id).first()

            if not tag:
                return jsonify({'message': 'tag não existe'}), 404
            
            db.session.add(tag)
            db.session.commit()

            response = jsonify({'message': 'tag apagada'})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response


add_tag_pos = api.model('Add_Tag_Post', {
    'tag_id': fields.Integer(required = True, description = 'ID da tag')
})

@api.route('/post/<int:id>')
class AddCategoryPost(Resource):
    @api.doc('add_tag_post')
    @api.expect(add_tag_pos)
    @jwt_required()
    def put(self, id):
        """Associa tag ao post"""
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:

            post = Posts.query.filter_by(id = id).first()

            tag_id = request.json['tag_id']

            tag_post = PostTags(tag_id = tag_id, post_id = post.id)
            db.session.add(tag_post)
            db.session.commit()

            response = jsonify({'message': 'tag adiciona'})
            response.status_code = 201
            return response
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response
