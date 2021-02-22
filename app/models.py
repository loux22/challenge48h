from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

image_tag = db.Table('image_tag',
                db.Column('image_id', db.Integer, db.ForeignKey(
                    'image.id'), primary_key=True),
                db.Column('tag_id', db.Integer, db.ForeignKey(
                    'tag.id'), primary_key=True),
                )

class Image(UserMixin, db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    typeImg = db.Column(db.String(255))
    isProduct = db.Column(db.Boolean)
    isHuman = db.Column(db.Boolean)
    isInstitutional = db.Column(db.Boolean)
    formatImg = db.Column(db.String(255))
    credit = db.Column(db.String(255))
    rightOfUse = db.Column(db.Boolean)
    copyrightImg = db.Column(db.String(255))
    endOfUse = db.Column(db.DateTime)
    tags = db.relationship('Tag', secondary=image_tag,
                           backref=db.backref('image_tag', lazy='dynamic'))
    category = db.relationship('Category', backref='image')


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Image {}>'.format(self.name)
    

class Tag(UserMixin, db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.relationship(
        'Image', secondary=image_tag, backref=db.backref('image_tag', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag {}>'.format(self.name)



class Category(UserMixin, db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    typeCategory = db.Column(db.String(255))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

