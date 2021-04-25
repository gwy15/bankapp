import logging
from decimal import Decimal
from flask import Blueprint, render_template, redirect, request
from flask.helpers import flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired, Length, Regexp
from flask_login import LoginManager, login_user

from bankapp.validators import DecimalValidator
from bankapp import exceptions, models

logger = logging.getLogger(__name__)

# login manager
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def redirect_to_login():
    return redirect(url_for('account.login', next=request.url))


# flask routers
bp = Blueprint('account', __name__)


class UserForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(), Length(min=1, max=127),
        Regexp(r'^[a-z0-9_\-\.]+$')
    ])
    password = StringField('password', validators=[
        DataRequired(), Length(min=1, max=127),
        Regexp(r'^[a-z0-9_\-\.]+$')
    ])


class RegisterForm(UserForm):
    balance = DecimalField('balance', validators=[
        DecimalValidator()
    ])


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    # POST
    if form.validate_on_submit():
        # register
        user: models.User
        try:
            user = models.User.create(
                form.username.data, form.password.data,
                balance=form.balance.data
            )
        except exceptions.UsernameTaken:
            flash('The username is already taken.')
            return render_template('register.html', form=form)

        login_user(user)
        return redirect('/')
    else:
        for name, msgs in form.errors.items():
            for msg in msgs:
                flash(f'{name} error: {msg}')

        return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # get the 'next' param from url so that the user can jump back
    next = request.args.get('next', default=url_for('index.index'))
    logger.info('next = %s', next)

    form = UserForm()
    if request.method == 'GET':
        return render_template('login.html', form=form, next=next)

    if not form.validate_on_submit():
        for name, msgs in form.errors.items():
            for msg in msgs:
                flash(f'{name} error: {msg}')

        return render_template('login.html', form=form, next=next)

    user: models.User
    try:
        user = models.User.try_from(
            form.username.data, form.password.data
        )
    except exceptions.UserDoesNotExistOrWrongPassword:
        flash('user does not exist or wrong password.')
        return render_template('login.html', form=form, next=next)

    login_user(user)
    logger.info(f'User {user.username} login success.')
    flash(f'Welcome, {user.username}')

    logger.info('next = %s', next)
    return redirect(next)


__ALL__ = ['bp']
