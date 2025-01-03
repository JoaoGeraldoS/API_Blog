from flask import Blueprint, request, jsonify
from app.models import Categories, PostCategory, db, Posts, Users
from flask_restx import Namespace, fields, Resource
from app.serializer import CategroySchema
from flask_jwt_extended import jwt_required, get_jwt_identity

rota_category = Blueprint('categories', __name__)
api = Namespace('categories', description = 'Operações categorias')

category_model = api.model('category', {
    'name': fields.String(required = True, description = 'Nome da categoria')
})


@api.route('/')
class CategoryDocumentation(Resource):
    @api.doc('create_category')
    @api.expect(category_model)
    @jwt_required()
    def post(self):
        """Cria categoria"""
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:
            name = request.json['name']

            for category in name:
                add_category = Categories(name = category)
                db.session.add(add_category)
                db.session.commit()
            
            response = jsonify({'message': 'Categoria registrada'})
            response.status_code = 201
            return response
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response
    

    @api.doc('read_category')
    def get(self):
        """Mostra categorias"""
        category = Categories.query.all()

        category_schema = CategroySchema(many = True)
        response = category_schema.jsonify(category)
        response.status_code = 200
        return response
    

@api.route('/<int:id>')
class SpecificCategory(Resource):
    @api.doc('update_category')
    @api.expect(category_model)
    @jwt_required()
    def put(self, id):
        """Atualiza categoria"""
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:
            category = Categories.query.filter_by(id = id).first()
            
            if not category:
                return jsonify({'message': 'categoria não encontrada'}), 404
            
            category.name = request.json['name']
            db.session.commit()

            response = jsonify({'message': 'categoria atualizada'})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response
    

    @api.doc('read_specific_category')
    def get(self, id):
        """Mostra categoria especifica"""
        category = Categories.query.filter_by(id = id).first()

        if not category:
            return jsonify({'message': 'categoria não existe'}), 404
        
        category_schema = CategroySchema()
        response = category_schema.jsonify(category)
        response.status_code = 200
        return response
    

    @api.doc('delete_category')
    @jwt_required()
    def delete(self, id):
        """Apaga categoria"""
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:
            category = Categories.query.filter_by(id = id).first()

            if not category:
                return jsonify({'message': 'categoria não existe'}), 404
            
            db.session.add(category)
            db.session.commit()

            response = jsonify({'message': 'categoria apagada'})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response


add_category_pos = api.model('Add_Category_Post', {
    'category_id': fields.Integer(required = True, description = 'ID do categoria')
})
    
@api.route('/post/<int:id>')
class AddCategoryPost(Resource):
    @api.doc('add_category_post')
    @api.expect(add_category_pos)
    @jwt_required()
    def put(self, id):
        """Adiciona categoria ao post"""
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:
            post = Posts.query.filter_by(id = id).first()

            category_id = request.json['category_id']

            category_post = PostCategory(category_id = category_id, post_id = post.id)
            db.session.add(category_post)
            db.session.commit()

            response = jsonify({'message': 'Categoria adiciona'})
            response.status_code = 201
            return response
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response
