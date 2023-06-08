from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from wtforms import MultipleFileField
from flask_ckeditor import CKEditorField


class AddArticleForm(FlaskForm):
    locations = SelectMultipleField('Локации', coerce=int)
    manufacturers = SelectMultipleField('Производители', coerce=int)
    title = StringField('Заголовок статьи', validators=[DataRequired()])
    content = CKEditorField('Текст', validators=[DataRequired()])  # TextAreaField('Текст', validators=[DataRequired()])
    rewiew = TextAreaField('Краткое описание', validators=[DataRequired()])
    tags = StringField('Теги')
    pictures = MultipleFileField('Фото', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Создать')


class AddCommentFrom(FlaskForm):
    text = TextAreaField('Текст сообщения')
    replied_to = TextAreaField()
    submit = SubmitField('Оставить комментарий')
