from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddColorForm(FlaskForm):
    color_code = StringField('Код цвета', validators=[DataRequired()])
    color_name = StringField('Название цвета', validators=[DataRequired()])
    submit = SubmitField('Добавить')
