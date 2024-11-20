from flask_marshmallow import Marshmallow

ma = Marshmallow()

from app.serializer.seiralizer_models import PostSchema
from app.serializer.seiralizer_models import CategroySchema
from app.serializer.seiralizer_models import TagsSchema
from app.serializer.seiralizer_models import UsersSchema
from app.serializer.seiralizer_models import CommentsSchema
from app.serializer.seiralizer_models import TagsPostsSchema
from app.serializer.seiralizer_models import CategoryPostSchema