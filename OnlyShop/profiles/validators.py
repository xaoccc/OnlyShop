from django.core.exceptions import ValidationError
from django.utils import timezone


def name_validator(value):
    if not value.isalpha():
        raise ValidationError("The name can contain only alphabetical characters!")
    if not value[0] == value[0].upper():
        raise ValidationError("The name must start with an uppercase letter!")



class UpperLowerCasePasswordValidator:
    def validate(self, password, user=None):
        if password == password.upper() or password == password.lower():
            raise ValidationError("This password must contain at least one uppercase and one lowercase character.")

    def get_help_text(self):
        return "Your password must contain at least one uppercase and one lowercase character."


class AlphaPasswordValidator:

    def validate(self, password, user=None):
        if password.isalpha():
            raise ValidationError("Your password can’t be entirely alphabetic.")

    def get_help_text(self):
        return "Your password can’t be entirely alphabetic."