from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from project.models import Article, Location, Manufacturer
import folium
import os
from geopy.geocoders import Nominatim


gmap = Blueprint('map', __name__, template_folder='templates/map', url_prefix='/map')


@gmap.route('/create')
def create_map():
    map = folium.Map(location=[45.263034195319385, 37.4354044603708], zoom_start=8)
    decoder = Nominatim(user_agent='tieworld')
    path = os.path.dirname(__file__)
    filepath = "/templates/map/map1.html"
    articles = Article.query.all()

    def colorpick(region):
        if region == "Кубанская область":
            return 'red'
        elif region == "Eкатеринославская губерния":
            return 'blue'
        elif region == "Таврическая губерния":
            return 'green'
        elif region == "Республика Крым":
            return 'green'
        elif region == "Ставропольская губерния":
            return 'black'
        elif region == "Терская область":
            return 'darkgreen'
        elif region == "Донская область":
            return 'orange'
        elif region == "Екатеринославская губерния":
            print("############################")
            return 'white'
        else:
            return 'red'

    locations = set()
    points = []
    for article in articles:
        locations.add(article.location)

    for loc in locations:
        located_manufactures = Article.query.filter_by(location=loc).all()
        header = ''
        point = []
        for man in located_manufactures:
            header += "|" + man.header
            region = man.region
        try:
            ll = list(decoder.geocode(loc).point)
            ll.pop()
            point.append([ll, header, region])
        except Exception as err:
            print(err)
        points.append(point)
    print(points)

    for point in points:
        print(point)
        folium.Marker(location=point[0][0], popup=point[0][1],
                      icon=folium.Icon(color=colorpick(point[0][2]))).add_to(map)

    map.save(path + filepath)

    return render_template('map1.html')


@gmap.route('/show')
def show_map():
    return render_template('map1.html')


@gmap.route('show/<int:location_id>')
def show_loc(location_id):
    loc = Location.query.get(location_id)
    articles = loc.articles
    map = folium.Map(location=[loc.lat, loc.long], zoom_start=12)
    label = '<ul>'
    for i in articles:
        label += f'\n<li><a href=/article/{i.id}>{i.title}</a></li>'
    label += '</ul>'
    folium.Marker(location=[loc.lat, loc.long], popup=label,
                  icon=folium.Icon(color=loc.color.color_name)).add_to(map)
    return render_template('show_loc.html', map=map._repr_html_())

@gmap.route('/all')
def show_all():
    locs = Location.query.all()
    map = folium.Map(location=[45.263034195319385, 37.4354044603708], zoom_start=7, width="100%", height='90%')
    for loc in locs:
        articles = loc.articles
        label = '<ul>'
        for i in articles:
            label += f'\n<li><a href=/article/{i.id}>{i.title}</a></li>'
        label += '</ul>'
        folium.Marker(location=[loc.lat, loc.long], popup=label,
                      icon=folium.Icon(color=loc.color.color_name)).add_to(map)
    return render_template('show_loc.html', map=map._repr_html_())