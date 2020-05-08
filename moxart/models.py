from werkzeug.security import generate_password_hash
from moxart import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(255), index=True)
    password = db.Column(db.String(255))
    bio = db.Column(db.Text)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    registered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_at = db.Column(db.DateTime, nullable=True)

    def __init__(self,
                username, email, password, confirmed=False,
                admin=False, confirmed_at=None):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, 'sha256')
        self.registered_at = datetime.utcnow()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_at = confirmed_at

    def __repr__(self):
        return '<User {}>'.format(self.username)
