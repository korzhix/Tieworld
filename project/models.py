from project import db
from datetime import datetime


class Recomendation(db.Model):
    __tablename__ = "recomendations"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    # media?
    def __init__(self, text):
        self.content = text


#
# class Comments(db.Model):
#     # author text created_at
#     pass
#
#
# class User(db.Model):
#     # login username pass_hash comments favourite
#     pass
#
#
# class UserGroups(db.Model):
#     pass
#
#
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
    location = db.relationship("Location", uselist=False, backref="color")

    def __init__(self, name: str, code: str):
        self.color_name = name
        self.color_code = code


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(64), nullable=False)
    district = db.Column(db.String(64))
    region = db.Column(db.String(64))
    country = db.Column(db.String(64))
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'))
    #color = db.relationship("Color", uselist=False, backref="location")
    manufacturers = db.relationship("Manufacturer",
                                    secondary=manufacturer_location,
                                    backref="locations")
