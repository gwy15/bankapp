"""
The module for access database.

This module handles data access with database, which should be a SQL database.
By default the bankapp will use a SQLite database named 'bankapp.db' use by
setting `SQLALCHEMY_DATABASE_URI` in config, it can also use other databases
like MySQL, MariaDB or PostgreSQL.

Internally the model provides two ORM classes: `User` and `TransactionRecord`.
"""
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
    bcrypt.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(127), nullable=False)
    balance_cents = db.Column(db.Integer, nullable=False)
    # one-to-many
    transactions = db.relationship(
        'TransactionRecord', backref='user', lazy=True)

    @staticmethod
    def create(username: str, password: str, balance: Decimal) -> 'User':
        """Create the user with given parameters.

        The input parameters must always be valid.
        """
        pw_hash = bcrypt.generate_password_hash(password)
        try:
            user = User(
                username=username, password=pw_hash,
                balance_cents=0
            )
            user.balance = balance
            db.session.add(user)

            # add transaction record
            trans = TransactionRecord.new(user, balance)
            db.session.add(trans)

            db.session.commit()

        except sqlalchemy.exc.IntegrityError as ex:
            # there's a unique constraint on the `username` field so if username
            # collides this exception will be raised. This guarantees that
            # no two users will have the same username.
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
        db.session.add(TransactionRecord.new(self, amount))
        db.session.commit()

    def make_withdraw(self, amount: Decimal):
        self.balance -= amount
        if self.balance < 0:
            db.session.rollback()
            raise ValueError('The user does not have enough balance.')
        db.session.flush([self])
        db.session.add(TransactionRecord.new(self, -amount))
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


class TransactionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    amount_cents = db.Column(db.Integer, nullable=False)
    after_amount_cents = db.Column(db.Integer, nullable=False)

    # user: User

    @staticmethod
    def new(user: User, amount: Decimal) -> 'TransactionRecord':
        after_amount = user.balance + amount
        trans = TransactionRecord(
            amount_cents=int(amount * 100),
            after_amount_cents=int(after_amount * 100)
        )
        trans.user = user
        return trans

    @property
    def type(self):
        if self.amount_cents > 0:
            return 'Deposit'
        return 'Withdraw'

    @property
    def amount(self) -> Decimal:
        return Decimal(self.amount_cents) * Decimal('0.01')

    @property
    def deposit_amount(self) -> str:
        return '$' + str(self.amount) if self.amount > 0 else ''

    @property
    def withdraw_amount(self) -> str:
        return '-$' + str(abs(self.amount)) if self.amount < 0 else ''
