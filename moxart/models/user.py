import uuid

from werkzeug.security import generate_password_hash
from moxart import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    registered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_at = db.Column(db.DateTime, default=None)

    def __init__(self,
                 public_id, username, email, password, confirmed=False,
                 admin=False, confirmed_at=None):
        self.public_id = public_id
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, 'sha256')
        self.registered_at = datetime.utcnow()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_at = confirmed_at

    def __repr__(self):
        return '<User {}>'.format(self.username)
