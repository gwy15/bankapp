# https://flask-wtf.readthedocs.io/en/stable/quickstart.html
from flask import Blueprint, render_template, redirect, request
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp

bp = Blueprint('account', __name__, template_folder='../../templates')


class RegisterForm(FlaskForm):
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
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # TODO: register
            flash('Register success.')
            return redirect('/')
        else:
            for name, msgs in form.errors.items():
                for msg in msgs:
                    flash(f'{name} error: {msg}')

            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


__ALL__ = ['bp']
