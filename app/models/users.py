from app.models import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = True)
    username = db.Column(db.String(100), nullable = True, unique=True)
    email = db.Column(db.String(255), nullable = True, unique = True)
    password = db.Column(db.String(255), nullable = True)

    author = db.Column(db.Boolean, default = False)

    post = db.relationship('Posts', back_populates='user', cascade='all, delete')
    comment = db.relationship('Comments', back_populates = 'user', cascade = 'all, delete')