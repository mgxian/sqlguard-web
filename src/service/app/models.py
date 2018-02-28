from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Role:
    DEV = 0
    MANAGER = 1
    ADMIN = 2


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))

    def __init__(self, **kargs):
        super(User, self).__init__(**kargs)
        if self.email == current_app.config['SQL_GUARD_ADMIN']:
            self.role_id = Role.ADMIN
        else:
            self.role_id = Role.DEV

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
