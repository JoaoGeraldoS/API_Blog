from flask import Flask
from app.models import db
from app.routes import posts, users, categories, tags, comments
from flask_restx import Api
from app.serializer import ma
from flask_jwt_extended import JWTManager
from app.config import DevelopmentConfig
from flask_migrate import Migrate


def create_app(config_class = DevelopmentConfig()):

    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    
    
    api = Api(app, version='1.0', description='API do Blog', doc='/docs')

    api.add_namespace(posts.api, path='/posts')
    api.add_namespace(categories.api, path='/categories')
    api.add_namespace(tags.api, path='/tags')
    api.add_namespace(users.api, path='/users')
    api.add_namespace(comments.api, path='/comments')


    db.init_app(app)
    ma.init_app(app)
    jwt = JWTManager(app)
    Migrate(app, db)

    

    app.register_blueprint(posts.rota_post)
    app.register_blueprint(users.rota_user)
    app.register_blueprint(categories.rota_category)
    app.register_blueprint(tags.rota_tag)
    app.register_blueprint(comments.rota_comment)

    return app