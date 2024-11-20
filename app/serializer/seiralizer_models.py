from app.serializer import ma
from app.models import Posts, Categories, Tags, PostCategory, PostTags, Users, Comments

class CategroySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categories
        fields = ('id', 'name')

class CategoryPostSchema(ma.SQLAlchemyAutoSchema):
    category = ma.Nested(CategroySchema)
    class Meta:
        model = PostCategory
        fields = ('id', 'category')

class TagsSchema(ma.Schema):
    class Meta:
        model = Tags
        fields = ('id', 'name')
       

class TagsPostsSchema(ma.Schema):
    tag = ma.Nested(TagsSchema)
    class Meta:
        model = PostTags
        fields = ('id', 'tag')


class UsersSchema(ma.Schema):
    class Meta:
        model = Users
        fields = ('id', 'name', 'author')

class PostSchema(ma.Schema):
    categories = ma.Nested(CategoryPostSchema, many = True)
    tags = ma.Nested(TagsPostsSchema, many = True)
    user = ma.Nested(UsersSchema)
    class Meta:
        model = Posts
        fields = ('id', 'title', 'content', 'created_at', 'categories', 'tags', 'user')

class CommentsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comments