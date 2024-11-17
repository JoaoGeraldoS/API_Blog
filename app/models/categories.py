from app.models import db

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = True)

    category = db.relationship('PostCategory', back_populates = 'get_category', cascade = 'all, delete')

class PostCategory(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    get_category = db.relationship('Categories', back_populates = 'category')

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post = db.relationship('Posts', back_populates = 'categories')
    