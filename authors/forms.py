from django.contrib.auth.models import User
from django import forms


def add_attr(field, name, value):
    existing_attr = field.widget.attrs.get(name, '')
    field.widget.attrs[name] = f'{existing_attr} {value}'.strip()


def add_placeholder(field, placeholder):
    add_attr(field, 'placeholder', placeholder)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Ex.: David')
        add_placeholder(self.fields['last_name'], 'Ex.: Anton')
        add_placeholder(self.fields['username'], 'Type your username here.')
        add_placeholder(self.fields['email'], 'Type your e-mail here.')

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password',
        ]
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'username': 'Required. 150 characters or less. Letters, numbers and @/./+/-/_ only.'
        }
        error_messages = {
            'username': {
                'required': 'This field cannot be empty.'
            }
        }
        widgets = {
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here.'
            })
        }

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Re-enter your password here.'
        }),
        error_messages={
            'required': 'The password cannot be empty.'
        },
        help_text='The password must have at least 1 character.'
    )
