from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired
from wtforms import widgets


# class CheckboxWidget(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()


class AddManufacturerForm(FlaskForm):
    manufacturer_name = StringField('Название производства', validators=[DataRequired()])
    literature = TextAreaField('Список литературы')
    manufacturer_other = TextAreaField('Статистические характеристики')
    locations = SelectMultipleField('Локации', coerce=int)#CheckboxWidget('Локации', coerce=int)
    submit = SubmitField('Подтвердить')