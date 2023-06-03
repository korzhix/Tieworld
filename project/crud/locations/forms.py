from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from project.models import Color


class AddLocationForm(FlaskForm):
    lat = FloatField('Широта', validators=[DataRequired()])
    long = FloatField('Долгота', validators=[DataRequired()])
    location_name = StringField('Название населенного пункта', validators=[DataRequired()])
    district = StringField('Район')
    region = StringField('Регион', validators=[DataRequired()])
    country = StringField('Страна', validators=[DataRequired()])
    color = SelectField('Выберете цвет', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить локацию')
