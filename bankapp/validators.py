import math
import re
from decimal import Decimal

from wtforms.validators import ValidationError
from wtforms.fields.core import DecimalField

from bankapp import constants


class DecimalValidator:
    def __init__(self, min=0) -> None:
        super().__init__()
        self.message = 'This input is invalid as currency amount.'
        self.min = min

    def __call__(self, form, field: DecimalField):
        value: Decimal = field.data

        # check for not present
        if value is None:
            raise ValidationError(self.message)

        # check for wrong format
        raw_data = field.raw_data[0]
        if not re.match(r'^[\d\.]+$', raw_data):
            raise ValidationError(self.message)

        # check for number range
        if value is None or math.isnan(value) or value < 0 or value > constants.MAX_BALANCE:
            raise ValidationError(self.message)

        # maximum 3 digits after dot
        if value.as_tuple().exponent <= -3:
            raise ValidationError(self.message)

        # check for minimum value
        if value < self.min:
            raise ValidationError(self.message)
