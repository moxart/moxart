import uuid

from werkzeug.security import generate_password_hash
from marshmallow import Schema, fields
from moxart import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(50), primary_key=True, unique=True, nullable=False, default=uuid.uuid4())
    user_public_id = db.Column(db.String(50), unique=True, nullable=False, default=uuid.uuid4())
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    registered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_at = db.Column(db.DateTime, default=None)

    # RELATIONSHIPS #
    post = db.relationship('Post', backref='user', lazy=True)
    profile = db.relationship('Profile', backref='profile', uselist=False)
    # # RELATIONSHIPS END #

    def __init__(self,
                 username, email, password, admin):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.admin = admin

    def __repr__(self):
        return '<User {}>'.format(self.username)


class UserSchema(Schema):
    user_public_id = fields.Str()
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()
    admin = fields.Boolean()
    registered_at = fields.DateTime()
    confirmed = fields.Boolean()
    confirmed_at = fields.DateTime()
