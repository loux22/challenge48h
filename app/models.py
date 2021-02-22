from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Test(UserMixin, db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User {}>'.format(self.username)

