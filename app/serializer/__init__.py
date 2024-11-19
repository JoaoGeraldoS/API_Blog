from flask_marshmallow import Marshmallow

ma = Marshmallow()

from app.serializer.seiralizer_models import PostSchema
from app.serializer.seiralizer_models import CategroySchema
from app.serializer.seiralizer_models import TagsSchema