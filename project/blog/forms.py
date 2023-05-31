from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from wtforms import MultipleFileField


class AddColorForm(FlaskForm):
    color_code = StringField('Код цвета', validators=[DataRequired()])
    color_name = StringField('Название цвета', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AddArticleForm(FlaskForm):

    # Location data
    lat = FloatField('Широта', validators=[DataRequired()])
    long = FloatField('Долгота', validators=[DataRequired()])
    location_name = StringField('Название населенного пункта', validators=[DataRequired()])
    district = StringField('Район')
    region = StringField('Регион', validators=[DataRequired()])
    country = StringField('Страна', validators=[DataRequired()])
    ## color pass to init

    # manufacturer data
    manufacturer_name = StringField('Название производства', validators=[DataRequired()])
    literature = TextAreaField('Список литературы')
    manufacturer_other = TextAreaField('Статистические характеристики')

    # create location_manufacturer obj

    # article data
    title = StringField('Заголовок статьи', validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[DataRequired()])
    rewiew = TextAreaField('Краткое описание', validators=[DataRequired()])
    tags = StringField('Теги')
    pictures = MultipleFileField('Фото', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Создать')

