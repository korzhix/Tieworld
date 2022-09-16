from project import db
from datetime import datetime
class Article(db.Model):


    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.Text)
    contents = db.Column(db.Text)
    repres = db.Column(db.Text)
    location = db.Column(db.Text)
    region = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    images = db.Column(db.String())

    def __init__(self, header, content, repres, location, region, images):

        self.header = header
        self.contents = content
        self.repres = repres
        self.location = location
        self.region = region
        self.images = images

