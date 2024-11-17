from app.models import db
from datetime import datetime, timezone

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    content = db.Column(db.Text, nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc))

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post = db.relationship('Posts', back_populates = 'comment')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', back_populates='comment')
