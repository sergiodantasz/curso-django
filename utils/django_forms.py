from re import compile

from django.core.exceptions import ValidationError


def add_attr(field, name, value):
    existing_attr = field.widget.attrs.get(name, '')
    field.widget.attrs[name] = f'{existing_attr} {value}'.strip()


def add_placeholder(field, placeholder):
    add_attr(field, 'placeholder', placeholder)


def is_strong_password(password):
    regex = compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError(
            'The password must have at least one uppercase letter, '
            'one lowercase letter, one number and at least 8 characters.',
            'invalid',
        )
