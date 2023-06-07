from flask import render_template, request, redirect, Blueprint, url_for, flash
from project.auth.forms import RegisterForm, LoginForm
from project import login_manager
from project.models import User
from project import db
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

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
                        first_name=form.first_name.name,
                        last_name=form.last_name.data,
                        password=form.password.data)
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
