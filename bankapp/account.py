# https://flask-wtf.readthedocs.io/en/stable/quickstart.html
from flask import Blueprint, render_template, redirect, request
from flask.helpers import flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp
from flask_login import LoginManager, login_user

from bankapp import models

bp = Blueprint('account', __name__, template_folder='../../templates')
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return models.User.get(user_id)


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
            # TODO: register
            user = models.User.create(form.username, form.password)
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
@login_manager.unauthorized_handler
def login():
    form = UserForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            for name, msgs in form.errors.items():
                for msg in msgs:
                    flash(f'{name} error: {msg}')

            return render_template('login.html', form=form)
        # TODO: validate
        user: models.User = models.User.try_from(form.username, form.password)

        login_user(user)
        flash(f'Welcome, {user.username}')
        next = request.args.get('next')
        if not next or not is_safe_url(next):
            next = url_for('index')

        return redirect(next)
    else:
        return render_template('login.html', form=form)


__ALL__ = ['bp']
