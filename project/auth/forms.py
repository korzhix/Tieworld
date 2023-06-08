from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    # email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_pass = PasswordField('Повторите пароль', validators=[EqualTo('password', message='Пароли должны совпадать.')])
    first_name = StringField('Имя')
    last_name = StringField('Фамилия')
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class UpdateProfileForm(FlaskForm):
    password = PasswordField('Новый Пароль', validators=[DataRequired()])
    first_name = StringField('Имя')
    last_name = StringField('Фамилия')
    submit = SubmitField('Обновить')
    repeat_pass = PasswordField('Повторите пароль', validators=[EqualTo('password', message='Пароли должны совпадать.')])
