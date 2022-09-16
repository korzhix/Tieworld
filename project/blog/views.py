from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from project import db, app
from flask import request
from project.models import Article
from project.blog.forms import AddArticleForm
from project.blog.picture_handler import add_pic

blog = Blueprint('blog', __name__, template_folder='templates/blog', url_prefix='/article')


@blog.route('/add_article', methods=['GET', 'POST'])
def add():

    form = AddArticleForm()

    if form.validate_on_submit():
        pics = request.files.getlist(form.pictures.name)
        paths = []
        if pics:
            for pic in pics:
                picture_contents = pic.stream.read()
                filepath = add_pic(pic_content=picture_contents, pic_name=pic.filename, title=form.header.data)
                paths.append(filepath)
        post = Article(header=form.header.data, content=form.content.data,
                       repres=form.repres.data, location=form.location.data, region=form.region.data,
                       images=str(paths))
        db.session.add(post)
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
