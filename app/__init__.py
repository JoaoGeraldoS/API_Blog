from flask import Flask
from app.models import db
from app.routes import posts, users, categories, tags, comments


def create_app(config_class = None):

    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(posts.api)
    app.register_blueprint(users.rota_user)
    app.register_blueprint(categories.rota_category)
    app.register_blueprint(tags.rota_tag)
    app.register_blueprint(comments.rota_comment)

    return app