from flask import render_template, request, redirect, Blueprint, url_for, flash, abort
from project.auth.forms import RegisterForm, LoginForm, UpdateProfileForm
from project import login_manager
from project.models import User, Comment
from project import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__, template_folder='templates/auth',
                 url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        if User.query.filter_by(username=form.username.data).first():
            msg = 'Такой логин уже существует'
            flash(msg)
        else:
            user = User(username=form.username.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        password=form.password.data, usergroup_id=2)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    elif request.method == 'POST':
        flash('Заполните форму.')

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.verify_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Неправильный логин или пароль')
    return render_template('login.html', form=form)


@auth.route('/me')
@login_required
def profile():
    comments = current_user.comments
    return render_template('profile.html', me=current_user, comments=comments)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@auth.route('edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_profile(user_id):
    if current_user.id != user_id:
        abort(403)
    else:
        user = load_user(user_id)
        form =UpdateProfileForm()
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            if form.password.data:
                user.password = form.password.data
            db.session.commit()
            return redirect(url_for('auth.profile'))
        elif request.method == 'GET':
            form = UpdateProfileForm()
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
        return render_template('update_profile.html', form=form)

@auth.route('/admin')
@login_required
def admin(mode='users'):
    if int(current_user.usergroup_id) != 1:
        abort(403)
    try:
        mode = request.args['mode']
    except:
        mode = 'users'
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.username).paginate(page=page, per_page=10)
    comments = Comment.query.order_by(Comment.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin.html', mode=mode, users=users, comments=comments)


@auth. route('/delete_user/<int:user_id>')
@login_required
def delete_user(id):
    if int(current_user.usergroup_id) != 1:
        abort(403)
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('auth.admin', mode='users'))


@auth.route('/delete_comment/<int:id>')
@login_required
def delete_comment(id):
    if int(current_user.usergroup_id) != 1:
        abort(403)
    comment = Comment.query.get(id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('auth.admin', mode='comments'))
