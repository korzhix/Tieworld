import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_ckeditor import CKEditor, upload_success, upload_fail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

db = SQLAlchemy(metadata=metadata, app=app)
Migrate(app, db)
ckeditor = CKEditor(app)


def init_db():
    db.create_all()
    db.session.commit()


from project.blog.views import blog
from project.map.views import gmap
from project.crud.locations.views import locations
from project.crud.colors.views import colors
from project.crud.manufacturers.views import manufacturers
app.register_blueprint(blog)
app.register_blueprint(gmap)
app.register_blueprint(locations)
app.register_blueprint(colors)
app.register_blueprint(manufacturers)

if __name__ == "__main__":
    init_db()
