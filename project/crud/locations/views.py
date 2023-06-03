from flask import render_template, Blueprint, flash, redirect, url_for, request
from project import db
from project.models import Location, Color
from project.crud.locations.forms import AddLocationForm
from datetime import datetime
from sqlalchemy.orm import joinedload

locations = Blueprint('locations', __name__, template_folder='templates/locations', url_prefix='/location')


@locations.route('/crud', methods=['GET', 'POST'])
def locations_crud():

    form = AddLocationForm()
    colors = Color.query.all()
    form.color.choices = [(c.id, c.color_name) for c in colors]
    if form.validate_on_submit():
        color_id = form.color.data
        color_instance = Color.query.get(color_id)
        location = Location(lat=form.lat.data, long=form.long.data, name=form.location_name.data,
                            district=form.district.data, region=form.region.data,
                            country=form.country.data, created_at=datetime.utcnow(), color=color_instance)
        db.session.add(location)
        db.session.commit()
        flash('Локация добавлена')
        return redirect(url_for('locations.locations_crud'))

    locs = Location.query.options(joinedload('manufacturers')).order_by(Location.created_at)
    return render_template('locations.html', locs=locs, form=form, type_of_action='Создать')


@locations.route('/update/<int:location_id>', methods=['GET', 'POST'])
def update(location_id):
    location = Location.query.get_or_404(location_id)
    locs = Location.query.options(joinedload('manufacturers')).order_by(Location.created_at)
    form = AddLocationForm()
    colors = Color.query.all()
    form.color.choices = [(c.id, c.color_name) for c in colors]
    if form.validate_on_submit():
        location.lat = form.lat.data
        location.long = form.long.data
        location.name = form.location_name.data
        location.region = form.region.data
        location.district = form.district.data
        location.country = form.country.data
        color_id = form.color.data
        color_instance = Color.query.get(color_id)
        location.color = color_instance
        db.session.commit()
        flash('Запись обновлена')
        return redirect(url_for('locations.locations_crud'))
    elif request.method == 'GET':
        form.lat.data = location.lat
        form.long.data = location.long
        form.location_name.data = location.name
        form.region.data = location.region
        form.district.data = location.district
        form.country.data = location.country
        return render_template('locations.html', locs=locs, form=form, type_of_action='Обновить')


@locations.route('/delete/<int:location_id>')
def delete(location_id):
    locaton = Location.query.get_or_404(location_id)
    db.session.delete(locaton)
    db.session.commit()
    flash('Локация удалена из списка')

    db.session.commit()
    return redirect(url_for('locations.locations_crud'))
