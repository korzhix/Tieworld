import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


def init_db():
    db.create_all()
    db.session.commit()


from project.blog.views import blog
from project.map.views import gmap
app.register_blueprint(blog)
app.register_blueprint(gmap)


if __name__ == "__main__":
    init_db()
