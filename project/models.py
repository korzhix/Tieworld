from project import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Recomendation(db.Model):
    __tablename__ = "recomendations"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    # media?
    def __init__(self, text):
        self.content = text


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    #email = db.Column(db.String(255), nullable=False, unique=True)
    #email_confirmed_at = db.Column(db.DateTime())
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean()),
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    comments = db.relationship('Comment', backref='author')

    @property
    def password(self):
        raise AttributeError('Password is not readable attribut')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.String(2048))
    created_at = db.Column(db.DateTime)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))


manufacturer_location = db.Table("manufacturer_location",
                                 db.Column('manufacturer_id', db.Integer, db.ForeignKey('manufacturers.id')),
                                 db.Column('location_id', db.Integer, db.ForeignKey('locations.id'))
                                 )
article_manufacturer = db.Table("article_manufacturer",
                                db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
                                db.Column('manufacturer_id', db.Integer, db.ForeignKey('manufacturers.id')),
                                )
article_location = db.Table('article_location',
                            db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
                            db.Column('location_id', db.Integer, db.ForeignKey('locations.id')),
                            )


class Manufacturer(db.Model):
    __tablename__ = "manufacturers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    literature = db.Column(db.String(1024))
    other = db.Column(db.String)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    contents = db.Column(db.Text)
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    tags = db.Column(db.String(256))
    images = db.Column(db.String)
    locations = db.relationship('Location', secondary=article_location, backref='articles')
    manufacturers = db.relationship('Manufacturer', secondary=article_manufacturer, backref='articles')
    comments = db.relationship('Comment', backref='article')

    def __init__(self, title, tags, content, repres, images, created_at=datetime.utcnow()):

        self.created_at = created_at
        self.title = title
        self.contents = content
        self.review = repres
        self.images = images
        self.tags = tags


class Color(db.Model):
    __tablename__ = "colors"
    id = db.Column(db.Integer, primary_key=True)
    color_code = db.Column(db.String(24))
    color_name = db.Column(db.String(24))
    locations = db.relationship("Location", backref="color")


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(64), nullable=False)
    district = db.Column(db.String(64))
    region = db.Column(db.String(64))
    country = db.Column(db.String(64))
    created_at = db.Column(db.DateTime)
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'))
    manufacturers = db.relationship("Manufacturer",
                                    secondary=manufacturer_location,
                                    backref="locations")
