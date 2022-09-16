from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from wtforms import MultipleFileField


class AddArticleForm(FlaskForm):

    header = StringField('Заголовок:', validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[DataRequired()])
    repres = StringField('Резюме')
    location = StringField('Геолокация производства')
    region = StringField('Регион производства')
    pictures = MultipleFileField('Фото', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Создать')

