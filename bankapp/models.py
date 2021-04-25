# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
from decimal import Decimal
from typing import Optional
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import flask
import sqlalchemy
from bankapp import constants, exceptions

logger = logging.getLogger(__name__)

db: SQLAlchemy = SQLAlchemy()
bcrypt: Bcrypt = Bcrypt()


def init_app(app: flask.Flask):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    bcrypt.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(127), nullable=False)
    balance_cents = db.Column(db.Integer, nullable=False)

    @staticmethod
    def create(username: str, password: str, balance: Decimal) -> 'User':
        """Create the user with given parameters
        """
        pw_hash = bcrypt.generate_password_hash(password)
        try:
            user = User(
                username=username, password=pw_hash,
                balance_cents=0
            )
            user.balance = balance

            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as ex:
            db.session.rollback()
            raise exceptions.UsernameTaken from ex
        assert user.id > 0
        logger.info(f'User {username} register success.')
        return user

    @staticmethod
    def try_from(username: str, password: str) -> 'User':
        """Try retrieve an user from database with given username and
        password. The given password is not hashed.
        """
        user = User.query.filter_by(username=username).first()
        if user is None:
            raise exceptions.UserDoesNotExistOrWrongPassword()

        if bcrypt.check_password_hash(user.password, password):
            return user
        raise exceptions.UserDoesNotExistOrWrongPassword()

    def make_deposit(self, amount: Decimal):
        self.balance += amount
        if self.balance > constants.MAX_BALANCE:
            db.session.rollback()
            raise ValueError('The balance overflowed.')
        db.session.flush([self])
        db.session.commit()

    def make_withdraw(self, amount: Decimal):
        self.balance -= amount
        if self.balance < 0:
            db.session.rollback()
            raise ValueError('The user does not have enough balance.')
        db.session.flush([self])
        db.session.commit()

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    @property
    def balance(self):
        return Decimal(self.balance_cents) * Decimal('0.01')

    @balance.setter
    def balance(self, value: Decimal):
        if not isinstance(value, Decimal):
            raise ValueError(
                f'Expected Decimal for balance, got {type(value)}.')
        if value < 0:
            raise exceptions.NegativeBalance()
        if value > constants.MAX_BALANCE:
            raise ValueError('The value is too big.')
        if value.as_tuple().exponent <= -3:
            raise ValueError('The decimal has too many digits.')

        self.balance_cents = int(value * 100)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
