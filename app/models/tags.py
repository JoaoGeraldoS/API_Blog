from app.models import db

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = True)

    tag = db.relationship('PostTags', back_populates = 'get_tag', cascade = 'all, delete')

class PostTags(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    get_tag = db.relationship('Tags', back_populates = 'tag')

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post = db.relationship('Posts', back_populates = 'tags')