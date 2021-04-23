import logging
from flask_wtf import FlaskForm
from wtforms import DecimalField

from bankapp.validators import DecimalValidator

logger = logging.getLogger(__name__)


class TransactionForm(FlaskForm):
    amount = DecimalField('amount', validators=[
        DecimalValidator()
    ])
