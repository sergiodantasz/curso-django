from re import compile

from django import forms
from django.contrib.auth.models import User
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
            'invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Ex.: David')
        add_placeholder(self.fields['last_name'], 'Ex.: Anton')
        add_placeholder(self.fields['username'], 'Ex.: DavidAnton_123')
        add_placeholder(self.fields['email'], 'Ex.: davidanton@email.com')
        add_placeholder(self.fields['password'], 'Type your password here.')
        add_placeholder(self.fields['password2'], 'Re-enter your password here.')

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password'
        ]

    username = forms.CharField(
        label='Username',
        error_messages={
            'required': 'The username cannot be empty.',
            'min_length': 'The username must have at least 4 characters.',
            'max_length': 'The user must have a maximum of 4 characters.',
        },
        help_text='Required. 150 characters or less. Letters, numbers and @.+-_ only.',
        min_length=4, max_length=150
    )

    email = forms.EmailField(
        label='E-mail',
        error_messages={
            'required': 'The e-mail cannot be empty.'
        }
    )

    first_name = forms.CharField(
        label='First name',
        error_messages={
            'required': 'The first name cannot be empty.'
        }
    )

    last_name = forms.CharField(
        label='Last name',
        error_messages={
            'required': 'The last name cannot be empty.'
        }
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'The password cannot be empty.'
        },
        help_text=(
            'The password must have at least one uppercase letter, one '
            'lowercase letter, one number and at least 8 characters.'
        ),
        validators=[is_strong_password]
    )

    password2 = forms.CharField(
        label='Re-enter password',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Please, re-enter the password.'
        },
        help_text=(
            'The password must have at least one uppercase letter, one '
            'lowercase letter, one number and at least 8 characters.'
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password2 != password:
            raise ValidationError({
                'password2': ValidationError(
                    'The passwords do not match.',
                    'invalid'
                )
            })
        return cleaned_data
