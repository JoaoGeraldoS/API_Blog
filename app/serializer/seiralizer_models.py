from app.serializer import ma
from app.models import Posts, Categories, Tags, PostCategory, PostTags, Users

class CategroySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categories

class CategoryPostSchema(ma.SQLAlchemyAutoSchema):
    category = ma.Nested(CategroySchema)
    class Meta:
        model = PostCategory
        fields = ('category',)

class TagsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tags

class TagsPostsSchema(ma.SQLAlchemyAutoSchema):
    tag = ma.Nested(TagsSchema)
    class Meta:
        model = PostTags
        fields = ('tag',)


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users

class PostSchema(ma.SQLAlchemyAutoSchema):
    categories = ma.Nested(CategoryPostSchema, many = True)
    tags = ma.Nested(TagsPostsSchema, many = True)
    user = ma.Nested(UsersSchema)
    class Meta:
        model = Posts
        fields = ('id', 'title', 'content', 'created_at', 'categories', 'tags', 'user')