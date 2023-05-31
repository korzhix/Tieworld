from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from project import db, app
from flask import request
from project.models import Article, Location,  Manufacturer #ManufacturerLocation
from project.blog.forms import AddArticleForm
from project.blog.picture_handler import add_pic
from datetime import datetime

blog = Blueprint('blog', __name__, template_folder='templates/blog', url_prefix='/article')


@blog.route('/add_article', methods=['GET', 'POST'])
def add():

    form = AddArticleForm()
    locations = Location.query.all()
    manufacturers = Manufacturer.query.all()
    ### КОСТЫЛЬ НА обработку искл-я картинок
    if form.validate_on_submit():
        pics = request.files.getlist(form.pictures.name)
        paths = []
        try:
            if pics:
                for pic in pics:
                    picture_contents = pic.stream.read()
                    filepath = add_pic(pic_content=picture_contents, pic_name=pic.filename, title=form.title.data)
                    paths.append(filepath)
        except:
            paths = ''
        # TODO:
        #  1) Значение по умолчанию для аргументов tags и не только
        post = Article(title=form.title.data, content=form.content.data, repres=form.rewiew.data,
                       created_at=datetime.utcnow(), images=str(paths), tags=form.tags.data)
        location = Location(lat=form.lat.data, long=form.long.data, name=form.location_name.data,
                            district=form.district.data, region=form.region.data,
                            country=form.country.data)

        data = '{' + str(form.manufacturer_other.data) + '}'
        manufacturer = Manufacturer(name=form.manufacturer_name.data,
                                    literature=form.literature.data,
                                    other=data)
        post.locations.append(location)
        post.manufacturers.append(manufacturer)
        location.manufacturers.append(manufacturer)

        db.session.add(post)
        db.session.add(location)
        db.session.add(manufacturer)
        db.session.commit()
        flash('Статья создана')
        # return render_template('add_article.html', form=form)
        return redirect(url_for('blog.list_articles'))

    return render_template('add_article.html', form=form)


@blog.route("/all")
def list_articles():
    page = request.args.get('page', 1, type=int)
    blog_posts = Article.query.order_by(Article.date.desc()).paginate(page=page, per_page=10)
    return render_template('articles.html', blog_posts=blog_posts)


@blog.route('<int:blog_post_id>')
def blog_post(blog_post_id):

    blog_post = Article.query.get_or_404(blog_post_id)
    images = blog_post.images[:-1].split(',')
    for i in range(0, len(images)):
        if i == 0:
            images[i] = images[i]
        images[i] = images[i][2:-1]

    return render_template('article.html', title=blog_post.header,
                            date=blog_post.date, post=blog_post, photo_list=images)


@blog.route('<int:blog_post_id>/delete')
def delete_article(blog_post_id):
    article = Article.query.get_or_404(blog_post_id)
    print(article)
    db.session.delete(article)
    db.session.commit()
    flash('Article has been deleted')

    db.session.commit()
    return redirect(url_for('blog.list_articles'))


@blog.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
def update(blog_post_id):
    article = Article.query.get_or_404(blog_post_id)

    form = AddArticleForm()
    if form.validate_on_submit():
        article.header = form.header.data
        article.contents = form.content.data
        article.location = form.location.data
        article.region = form.region.data
        db.session.commit()
        flash('Запись обновлена')
        return redirect(url_for('blog.blog_post', blog_post_id=article.id))
    elif request.method == 'GET':
        form.header.data = article.header
        form.content.data = article.contents
        form.location.data = article.location
        form.location.data = article.location
        form.region.data = article.region
    return render_template('add_article.html', title='Update',
                           form=form)
