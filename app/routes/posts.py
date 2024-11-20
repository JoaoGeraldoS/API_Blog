from flask import Blueprint, jsonify, request
from app.models import db, Posts, Categories, Tags, Users, PostCategory, PostTags
from app.utils import add_category, add_tag
from sqlalchemy.orm import joinedload
from app.serializer import PostSchema, TagsPostsSchema
from flask_restx import Namespace, fields, Resource
from datetime import datetime, timezone
from flask_jwt_extended import jwt_required, get_jwt_identity


rota_post = Blueprint('posts',__name__)
api = Namespace('posts', description='Operação dos posts')


post_model = api.model('Post', {
    'title': fields.String(required=True, description='Titulo do post'),
    'content': fields.String(required=True, description='Conteudo do post'),
    'author_id': fields.Integer(required=True, description='ID do author do post'),
    'categories': fields.List(fields.String, required = True, description='Lista de categorias'),
    'tags': fields.List(fields.String, required = True, description='Lista de tags')
})


@api.route('/')
class PostsDocuments(Resource):

    @api.doc('cerate_post')
    @api.expect(post_model)
    @jwt_required()
    def post(self):
        """Cria posts"""
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:
            
            title = request.json['title']
            content = request.json['content']
            author_id = request.json['author_id']
            categories = request.json.get('categories', [])
            tags = request.json.get('tags', [])

            print(categories)

            post = Posts(title = title, content = content, author_id = author_id)

            db.session.add(post)
            db.session.commit()

            
            for category in categories:
                get_categories = Categories.query.filter_by(name = category).first()
                if not get_categories:
                    add_category(post_id=post.id, category=category, categories=None)
                else:
                    add_category(post_id=post.id, category=category, categories=get_categories.id)
            

            for tag in tags:
                get_tags = Tags.query.filter_by(name = tag).first()
                if not get_tags:
                    add_tag(post_id=post.id, tag=tag, tags=None)
                else:
                    add_tag(post_id=post.id, tag=tag, tags=get_tags.id)

            response =  jsonify({'message': 'post criado'})
            response.status_code = 201
            return response
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response


    @api.doc('read_posts')
    def get(self):
        """Ler  posts"""
        posts = Posts.query.options(
            joinedload(Posts.categories).joinedload(PostCategory.get_category),  # Inclui categoria
            joinedload(Posts.tags).joinedload(PostTags.get_tag),                # Inclui tag
            joinedload(Posts.user)                                          # Inclui usuário
        ).all()

        

        post_schema = PostSchema(many = True)
        return post_schema.jsonify(posts)
    

update_post_model = api.model('UpdatePost', {
    'title': fields.String(required=False, description='Título do post'),
    'content': fields.String(required=False, description='Conteúdo do post')
})


@api.route('/<int:id>')
class SpecificPost(Resource):
    @api.doc('read_specific_post')
    def get(self, id):
        """Post especifico"""
        post = Posts.query.options(
            joinedload(Posts.categories),
            joinedload(Posts.tags),
            joinedload(Posts.user)
        ).filter_by(id = id).first()

        post_schema = PostSchema()
        response = post_schema.jsonify(post)
        response.status_code = 200
        return response
    
    @api.doc('update_post')
    @api.expect(update_post_model)
    @jwt_required()
    def put(self, id):
        """Atualiza post"""
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:

            post = Posts.query.filter_by(id = id).first()

            if not post:
                return jsonify({'message': 'Post não encontrado!'}), 404
            
            post.title = request.json['title']
            post.content = request.json['content']
            post.updated_at = datetime.now(timezone.utc)

            db.session.commit()

            response = jsonify({'message': 'Post atualizado'})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response
    
    @api.doc('delete_post')
    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        user = Users.query.filter_by(username = current_user).first()
        
        if user.author:
            post = Posts.query.filter_by(id = id).first()
            

            if not post:
                return jsonify({'message': 'Post não encontrado!'}), 404
            
            db.session.delete(post)
            db.session.commit()

            response = jsonify({'message': 'Post deletado'})
            response.status_code = 200
            return response
        
        else:
            response = jsonify({'message': 'Sem permissao'})
            response.status_code = 401
            return response

filter_model = api.model('Filter', {
    'category': fields.String(required = True, description='Filtro por categoria'),
    'tag': fields.String(required = True, description='Filtro por tag'),
    'author': fields.String(required = True, description='Filtro por autor'),

})



@api.route('/filter')
class FilterPost(Resource):
    @api.doc('filter')
    @api.expect(filter_model)
    def get(self):
          # Recuperar parâmetros de consulta
        category_name = request.args.get('category')
        tag_name = request.args.get('tag')
        author_name = request.args.get('author')

        

        # Base da consulta
        query = Posts.query

        # Aplicar os filtros
        if category_name:
            # query = query.filter(Posts.categories.any(name=category_name))
            query = query.join(PostCategory).join(Categories).filter(category_name == Categories.name)
           
            
        if tag_name:
            query = query.filter(Posts.tags.any(name=tag_name))
        if author_name:
            query = query.filter(Posts.author.has(username=author_name))

        query = query.options(joinedload(Posts.categories))
        print(query)
        # Executar a consulta
        posts = query.all()
        

        # Serializar os resultados com Marshmallow
        post_schema = PostSchema(many = True)
        response = post_schema.jsonify(posts)
        response.status_code = 200
        return response
