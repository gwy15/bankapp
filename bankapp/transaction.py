from decimal import Decimal
import logging
from flask import Blueprint, request, flash
from flask.templating import render_template
from flask_wtf import FlaskForm
from flask_login import login_required, current_user
from wtforms import DecimalField

from bankapp.validators import DecimalValidator
from bankapp import constants, models

logger = logging.getLogger(__name__)

# flask routers
bp = Blueprint('transaction', __name__)


class TransactionForm(FlaskForm):
    amount = DecimalField('amount', validators=[
        DecimalValidator(min=Decimal('0.01'))
    ])


@bp.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    form = TransactionForm()
    if request.method == 'GET':
        return render_template('deposit.html', form=form)
    # POST
    if not form.validate_on_submit():
        for name, msgs in form.errors.items():
            for msg in msgs:
                flash(f'{name} error: {msg}')
        return render_template('deposit.html', form=form)

    amount = form.amount.data

    # verify current balance
    # decimal does not overflow.
    if current_user.balance + amount > constants.MAX_BALANCE:
        flash('The balance is too big.')
        return render_template('deposit.html', form=form)

    # ok, make deposit
    current_user.make_deposit(amount)
    flash('Deposit success.')
    return render_template('deposit.html', form=form)


@bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    form = TransactionForm()
    if request.method == 'GET':
        return render_template('withdraw.html', form=form)
    # POST
    if not form.validate_on_submit():
        for name, msgs in form.errors.items():
            for msg in msgs:
                flash(f'{name} error: {msg}')
        return render_template('withdraw.html', form=form)

    amount = form.amount.data

    # verify current balance
    # decimal does not overflow.
    if current_user.balance < amount:
        flash('You don\'t have enough balance to make this withdraw.')
        return render_template('withdraw.html', form=form)

    # ok, make withdraw
    current_user.make_withdraw(amount)
    flash('Withdraw success.')
    return render_template('withdraw.html', form=form)


@bp.route('/transactions', methods=['GET'])
@login_required
def transactions():
    trans = (models.TransactionRecord
             .query
             .filter(models.TransactionRecord.user_id == current_user.id)
             .order_by(models.TransactionRecord.id.desc())
             .limit(15)
             .all()
             )

    return render_template(
        'transactions.html',
        transactions=trans
    )
