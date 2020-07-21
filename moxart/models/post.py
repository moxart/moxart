import uuid

from marshmallow import Schema, fields
from moxart import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    post_public_id = db.Column(db.String(50), unique=True, nullable=False)
    user_public_id = db.Column(db.String(50), db.ForeignKey('user.user_public_id'))
    category_public_id = db.Column(db.String(50), db.ForeignKey('category.category_public_id'))
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    published_at = db.Column(db.DateTime, nullable=False)

    # FOREIGN KEYS #
    # `user_public_id` #
    # `category_public_id` #
    # END FOREIGN KEYS #

    def __init__(self, user_public_id, category_public_id, title, content):
        self.id = uuid.uuid4()
        self.user_public_id = user_public_id
        self.post_public_id = uuid.uuid4()
        self.category_public_id = category_public_id
        self.title = title,
        self.content = content,
        self.published_at = datetime.utcnow()

    def __repr__(self):
        return '<Post {}>'.format(self.post_public_id)


class PostSchema(Schema):
    post_public_id = fields.Str()
    title = fields.Str()
    content = fields.Str()
    published_at = fields.DateTime()
