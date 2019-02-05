from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class DigitUsernameValidator(validators.RegexValidator):
    regex = r'^[\d]+$'
    message = _(
        'Enter a valid netid. This value may contain only numbers.'
    )
    flags = 0
