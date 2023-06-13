from flask import render_template, url_for, flash, redirect, request, Blueprint, abort, current_app
from project import db, app
from flask import request
from project.models import Article, Location, Manufacturer, Comment
from project.blog.forms import AddArticleForm, AddCommentFrom, FilterForm
from project.blog.picture_handler import add_pic
from datetime import datetime
from flask_ckeditor import upload_success, upload_fail
import os
from flask_login import current_user
from sqlalchemy.orm import selectinload, joinedload, Query
from sqlalchemy import and_
blog = Blueprint('blog', __name__, template_folder='templates/blog', url_prefix='/article')


@blog.route('/add', methods=['GET', 'POST'])
def add():
    form = AddArticleForm()
    last_created = Article.query.order_by(Article.created_at.desc()).limit(5)
    locs = Location.query.all()
    form.locations.choices = [(l.id, l.name) for l in locs]
    mans = Manufacturer.query.all()
    form.manufacturers.choices = [(m.id, m.name) for m in mans]
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
        location_ids = form.locations.data
        manufacturer_ids = form.manufacturers.data
        post = Article(title=form.title.data, content=form.content.data, repres=form.rewiew.data,
                       created_at=datetime.utcnow(), images=str(paths), tags=form.tags.data)

        for i in location_ids:
            loc = Location.query.get(i)
            post.locations.append(loc)
        for i in manufacturer_ids:
            man = Manufacturer.query.get(i)
            post.manufacturers.append(man)

        db.session.add(post)
        db.session.commit()
        #flash('Статья создана')
        # return render_template('add_article.html', form=form)
        return redirect(url_for('blog.list_articles'))

    return render_template('add_article.html', form=form, latest=last_created)


@blog.route("/all", methods=['GET', 'POST'])
def list_articles():
    filter_form = FilterForm()
    locations = Location.query.all()
    manufacturers = Manufacturer.query.all()
    filter_form.region.choices = [(c.region, c.region) for c in locations]
    filter_form.district.choices = [(c.district, c.district) for c in locations]
    filter_form.location_name.choices = [(c.name, c.name) for c in locations]
    filter_form.manufacturer_name.choices = [(c.name, c.name) for c in manufacturers]
    page = request.args.get('page', 1, type=int)
    blog_posts = Article.query.order_by(Article.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('articles.html', blog_posts=blog_posts, filter_form=filter_form)


@blog.route('/filter')
def filter_result():
    if request.args:
        filter_form = FilterForm()
        page = request.args.get('page', 1, type=int)
        regions = [r for r in request.args.getlist('region')]
        districts = [d for d in request.args.getlist('district')]
        locs = [l for l in request.args.getlist('location_name')]
        try:
            request.args['manufacturer_name']
            names = [r for r in request.args.getlist('manufacturer_name')]
            articles = Article.query.join(Article.locations).filter(and_(Location.region.in_(regions),
                                                                         Location.district.in_(districts),
                                                                         Location.name.in_(locs))).join(\
                Article.manufacturers).filter(Manufacturer.name.in_(names)).paginate(page=page, per_page=10)
        except Exception as err:
            articles = Article.query.join(Article.locations).filter(and_(Location.region.in_(regions),
                                                                         Location.district.in_(districts),
                                                                         Location.name.in_(locs))).paginate(page=page, per_page=10)
        return render_template('articles.html', blog_posts=articles, filter_form=filter_form)


@blog.route("/search")
def w_search():
    filter_form = FilterForm()
    locations = Location.query.all()
    manufacturers = Manufacturer.query.all()
    filter_form.region.choices = [(c.region, c.region) for c in locations]
    filter_form.district.choices = [(c.district, c.district) for c in locations]
    filter_form.location_name.choices = [(c.name, c.name) for c in locations]
    filter_form.manufacturer_name.choices = [(c.name, c.name) for c in manufacturers]
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query')
    blog_posts = Article.query.msearch(query, fields=['title', 'contents']).order_by(Article.created_at.desc()).paginate(page=page, per_page=10)

    return render_template('articles.html', blog_posts=blog_posts, filter_form=filter_form)

@blog.route('<int:blog_post_id>', methods=['GET', 'POST'])
def blog_post(blog_post_id, page=1):
    blog_post = Article.query.get_or_404(blog_post_id)
    images = blog_post.images[:-1].split(',')
    form = AddCommentFrom()
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(article_id=blog_post_id).paginate(page=page, per_page=10)

    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(text=form.text.data)
        comment.author = current_user
        comment.article = blog_post
        comment.created_at = datetime.utcnow()
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blog.blog_post', blog_post_id=blog_post_id))
    for i in range(0, len(images)):
        if i == 0:
            images[i] = images[i]
        images[i] = images[i][2:-1]

    return render_template('article.html', form=form, title=blog_post.title,
                           date=blog_post.created_at, post=blog_post, photo_list=images, comments=comments)


@blog.route('delete/<int:blog_post_id>')
def delete_article(blog_post_id):
    article = Article.query.get_or_404(blog_post_id)
    db.session.delete(article)
    db.session.commit()
    flash('Article has been deleted')

    db.session.commit()
    return redirect(url_for('blog.list_articles'))


@blog.route('/update/<int:blog_post_id>', methods=['GET', 'POST'])
def update(blog_post_id):
    article = Article.query.get_or_404(blog_post_id)
    form = AddArticleForm()
    locs = Location.query.all()
    form.locations.choices = [(l.id, l.name) for l in locs]
    mans = Manufacturer.query.all()
    form.manufacturers.choices = [(m.id, m.name) for m in mans]
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
        location_ids = form.locations.data
        manufacturer_ids = form.manufacturers.data
        article.contents = form.content.data
        article.review = form.rewiew.data
        article.images = str(paths)
        article.tags = form.tags.data
        for i in location_ids:
            loc = Location.query.get(i)
            article.locations.append(loc)
        for i in manufacturer_ids:
            man = Manufacturer.query.get(i)
            article.manufacturers.append(man)
        db.session.commit()
        return redirect(url_for(f'blog.blog_post', blog_post_id=article.id))
    elif request.method == 'GET':
        form.title.data = article.title
        form.tags.data = article.tags
        form.content.data = article.contents
        form.rewiew.data = article.review
        form.pictures.data = article.images
        db.session.add(article)
        db.session.commit()
        return render_template('add_article.html', form=form, latest=[])




#
# @app.route('/files/<path:filename>')
# def uploaded_files(filename):
#     path = '/the/uploaded/directory'
#     return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    filepath = os.path.join(current_app.root_path, 'static\post_photos')
    f.save(filepath)
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)
