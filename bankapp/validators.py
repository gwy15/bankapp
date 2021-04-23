from decimal import Decimal
import math
import re

from wtforms.validators import ValidationError
from wtforms.fields.core import DecimalField


class DecimalValidator(object):
    def __init__(self) -> None:
        super().__init__()
        self.message = 'This number is invalid as currency amount.'

    def __call__(self, form, field: DecimalField):
        value = field.data

        if value is None:
            raise ValidationError(self.message)

        raw_data = field.raw_data[0]
        if not re.match(r'^[\d\.]+$', raw_data):
            raise ValidationError(self.message)

        if value is None or math.isnan(value) or value < 0 or value > Decimal('4294967295.99') or \
                value.as_tuple().exponent <= -3:
            raise ValidationError(self.message)
