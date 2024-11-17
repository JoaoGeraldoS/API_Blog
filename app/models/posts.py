from app.models import db
from datetime import datetime, timezone

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = True)
    content = db.Column(db.Text, nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('Users', back_populates='post')
    categories = db.relationship('PostCategory', back_populates = 'post', cascade = 'all, delete')
    tags = db.relationship('PostTags', back_populates = 'post', cascade = 'all, delete')
    comment = db.relationship('Comments', back_populates = 'post', cascade = 'all, delete')

     