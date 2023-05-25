from project import db
from datetime import datetime


class Recomendation(db.Model):
    __tablename__ = "recomendations"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    # media?
    def __init__(self, text):
        self.content = text


class Comments(db.Model):
    # author text created_at
    pass


class User(db.Model):
    # login username pass_hash comments favourite
    pass


class UserGroups(db.Model):
    pass


manufacturer_location = db.Table(
    "manufacturer_location",
    db.Column("manufacturer_id",
              db.Integer,
              db.ForeignKey("manufacturers.id"),
              primary_key=True
              ),
    db.Column("location_id",
              db.Integer,
              db.ForeignKey("locations.id"),
              primary_key=True
              ),
    db.Column("article_id",
              db.Integer,
              db.ForeignKey("articles.id")
              ),
    db.Column("article",
              db.relationship("Article", back_populates="article")
              )
)


class Manufacturer(db.Model):
    __tablename__ = "manufacturers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    literature = db.Column(db.String(1024))
    other = db.Column(db.String())
    locations = db.relationship("Location",
                                secondary=manufacturer_location,
                                back_populates="manufacturers")

    def __init__(self, name, lit, other):
        self.name = name
        self.literature = lit
        self.other = other

class UserGroup(db.Model):
    pass


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(128))
    contents = db.Column(db.Text)
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tags = db.Column(db.String(256))
    locations_manufacturers = db.relationship("manufacturer_location",
                                              back_populates="article")
    images = db.Column(db.String())

    def __init__(self, header, tags, content, repres, location, region, images):
        self.header = header
        self.contents = content
        self.review = repres
        self.location = location
        self.region = region
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
    # ALT LONG NAME rayon region color contry
    alt = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(64), nullable=False)
    district = db.Column(db.String(64))
    region = db.Column(db.String(64))
    country = db.Column(db.String(64))
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'))
    color = db.relationship("Color", userlist=False, backref="location")
    manufacturers = db.relationship("Manufacturer",
                                    secondary=manufacturer_location,
                                    back_populates="locations")

    def __int__(self, alt: float, lg: float, name: str, distr: str,
                reg: str, country: str, color: Color):
        self.region = reg
        self.name = name
        self.alt = alt
        self.long = lg
        self.district = distr
        self.country = country
        self.color = color

# location_manufacturer -> year_of_foundation
# дополнительно у сведений производства
#