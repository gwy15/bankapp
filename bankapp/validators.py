import math
import re
from decimal import Decimal

from wtforms.validators import ValidationError
from wtforms.fields.core import DecimalField

from bankapp import constants

class DecimalValidator:
    def __init__(self, min=0) -> None:
        super().__init__()
        self.message = 'This number is invalid as currency amount.'
        self.min = min

    def __call__(self, form, field: DecimalField):
        value: Decimal = field.data

        if value is None:
            raise ValidationError(self.message)

        raw_data = field.raw_data[0]
        if not re.match(r'^[\d\.]+$', raw_data):
            raise ValidationError(self.message)

        if value is None or math.isnan(value) or value < 0 or value > constants.MAX_BALANCE or \
                value.as_tuple().exponent <= -3:
            raise ValidationError(self.message)

        if value < self.min:
            raise ValidationError(self.message)
