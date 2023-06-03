from flask import render_template, Blueprint, flash, redirect, url_for, request
from project import db
from project.models import Color
from project.crud.colors.forms import AddColorForm
from sqlalchemy.orm import joinedload

colors = Blueprint('colors', __name__, template_folder='templates/colors', url_prefix='/color')


@colors.route('/crud', methods=['GET', 'POST'])
def colors_crud():
    form = AddColorForm()
    if form.validate_on_submit():
        color = Color(color_code=form.color_code.data,
                      color_name=form.color_name.data)
        db.session.add(color)
        db.session.commit()
        flash('Цвет добавлен')
        return redirect(url_for('colors.colors_crud'))

    colors = Color.query.options(joinedload('locations'))
    return render_template('colors.html', colors=colors, form=form, type_of_action='Создать')


@colors.route('/update/<int:color_id>', methods=['GET', 'POST'])
def update(color_id):
    color = Color.query.get_or_404(color_id)
    cls = Color.query.options(joinedload('locations'))
    form = AddColorForm()
    if form.validate_on_submit():
        color.color_name = form.color_name.data
        color.color_code = form.color_code.data
        db.session.commit()
        flash('Запись обновлена')
        return redirect(url_for('colors.colors_crud'))
    elif request.method == 'GET':
        form.color_code.data = color.color_code
        form.color_name.data = color.color_name
        return render_template('colors.html', colors=cls, form=form, type_of_action='Обновить')


@colors.route('/delete/<int:color_id>')
def delete(color_id):
    color = Color.query.get_or_404(color_id)
    db.session.delete(color)
    db.session.commit()
    flash('Цвет удален из списка')

    db.session.commit()
    return redirect(url_for('colors.colors_crud'))
