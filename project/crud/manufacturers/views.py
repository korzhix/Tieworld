from flask import render_template, Blueprint, flash, redirect, url_for, request
from project import db
from project.models import Location, Color, Manufacturer, Article
from project.crud.manufacturers.forms import AddManufacturerForm
from sqlalchemy.orm import joinedload

manufacturers = Blueprint('manufacturer', __name__, template_folder='templates/manufacturers',
                          url_prefix='/manufacturer')


@manufacturers.route('/crud', methods=['GET', 'POST'])
def manufacturer_crud():
    form = AddManufacturerForm()
    locs = Location.query.all()
    form.locations.choices = [(l.id, l.name) for l in locs]
    if form.validate_on_submit():
        location_ids = form.locations.data
        #location_instances = Location.query.filter(Location.id in location_ids).all()
        manufacturer = Manufacturer(name=form.manufacturer_name.data, literature=form.literature.data,
                                    other=form.manufacturer_other.data)
        for i in location_ids:
            loc = Location.query.get(i)
            manufacturer.locations.append(loc)
        db.session.add(manufacturer)
        db.session.commit()
        flash('Производитель добавлен')
        return redirect(url_for('manufacturer.manufacturer_crud'))

    mans = Manufacturer.query.options(joinedload('locations'), joinedload('articles')).order_by(Manufacturer.name)
    return render_template('manufacturer.html', mans=mans, form=form, type_of_action='Создать')


@manufacturers.route('/update/<int:manufacturer_id>', methods=['GET', 'POST'])
def update(manufacturer_id):
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    mans = Manufacturer.query.options(joinedload('locations')).order_by(Manufacturer.name)
    form = AddManufacturerForm()
    locations = Location.query.all()
    form.locations.choices = [(l.id, l.name) for l in locations]
    if form.validate_on_submit():
        manufacturer.name = form.manufacturer_name.data
        manufacturer.other = form.manufacturer_other.data
        manufacturer.literature = form.literature.data
        location_ids = form.locations.data
        for i in location_ids:
            loc = Location.query.get(i)
            manufacturer.locations.append(loc)
        db.session.commit()
        flash('Запись обновлена')
        return redirect(url_for('manufacturer.manufacturer_crud'))
    elif request.method == 'GET':
        form.manufacturer_name.data = manufacturer.name
        form.manufacturer_other.data = manufacturer.other
        form.literature.data = manufacturer.literature
        form.locations.data = manufacturer.locations
        return render_template('manufacturer.html', mans=mans, form=form, type_of_action='Обновить')


@manufacturers.route('/delete/<int:manufacturer_id>')
def delete(manufacturer_id):
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    db.session.delete(manufacturer)
    db.session.commit()
    flash('Производитель удален из списка')

    db.session.commit()
    return redirect(url_for('manufacturer.manufacturer_crud'))
