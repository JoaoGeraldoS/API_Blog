from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.posts import Posts
from app.models.users import Users
from app.models.categories import Categories, PostCategory
from app.models.tags import Tags, PostTags
from app.models.comments import Comments