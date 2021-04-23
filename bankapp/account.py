import logging
from flask import Blueprint, render_template, redirect, request
from flask.helpers import flash, url_for
from flask_wtf import FlaskForm
import sqlalchemy
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp
from flask_login import LoginManager, login_user

from bankapp import exceptions, models

logger = logging.getLogger(__name__)
login_manager = LoginManager()

bp = Blueprint('account', __name__)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()


class UserForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(), Length(min=3, max=20),
        Regexp(r'[a-zA-Z0-9@\._\-]+')
    ])
    password = StringField('password', validators=[
        DataRequired(), Length(min=9, max=36),
        Regexp(r'[a-zA-Z0-9!@#$%\^&*\(\)\-_=\+]+')]
    )


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # register
            user: models.User
            try:
                user = models.User.create(
                    form.username.data, form.password.data)
            except exceptions.UsernameTaken:
                flash('The username is already taken.')
                return render_template('register.html', form=form)

            login_user(user)
            flash('Register success.')
            return redirect('/')
        else:
            for name, msgs in form.errors.items():
                for msg in msgs:
                    flash(f'{name} error: {msg}')

            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            for name, msgs in form.errors.items():
                for msg in msgs:
                    flash(f'{name} error: {msg}')

            return render_template('login.html', form=form)

        user: models.User
        try:
            user = models.User.try_from(
                form.username.data, form.password.data
            )
        except exceptions.UserDoesNotExistOrWrongPassword:
            flash('user does not exist or wrong password.')
            return render_template('login.html', form=form)

        login_user(user)
        logger.info(f'User {user.username} logined.')
        flash(f'Welcome, {user.username}')
        next = request.args.get('next')
        if not next or not is_safe_url(next):
            next = url_for('index.index')

        return redirect(next)
    else:
        return render_template('login.html', form=form)


@login_manager.unauthorized_handler
def redirect_to_login():
    return redirect(url_for('account.login'))


__ALL__ = ['bp']
