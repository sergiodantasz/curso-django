from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ('first_name', 'Ex.: David'),
            ('last_name', 'Ex.: Anton'),
            ('username', 'Ex.: DavidAnton_123'),
            ('email', 'Ex.: davidanton@email.com'),
            ('password', 'Type your password here.'),
            ('password2', 'Re-enter your password here.')
        ]
    )
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand(
        [
            ('username', 'Required. 150 characters or less. Letters, numbers and @.+-_ only.'),
            ('password', (
                'The password must have at least one uppercase letter, one '
                'lowercase letter, one number and at least 8 characters.'
            )),
            ('password2', (
                'The password must have at least one uppercase letter, one '
                'lowercase letter, one number and at least 8 characters.'
            ))
        ]
    )
    def test_fields_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current_help_text = form[field].field.help_text
        self.assertEqual(current_help_text, help_text)

    @parameterized.expand(
        [
            ('first_name', 'First name'),
            ('last_name', 'Last name'),
            ('username', 'Username'),
            ('email', 'E-mail'),
            ('password', 'Password'),
            ('password2', 'Re-enter password')
        ]
    )
    def test_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            'username': 'User',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@email.com',
            'password': 'Str0ngP@ssw0rd',
            'password2': 'Str0ngP@ssw0rd',
        }
        return super().setUp()

    @parameterized.expand(
        [
            ('username', 'The username cannot be empty.'),
            ('email', 'The e-mail cannot be empty.'),
            ('first_name', 'The first name cannot be empty.'),
            ('last_name', 'The last name cannot be empty.'),
            ('password', 'The password cannot be empty.'),
            ('password2', 'Please, re-enter the password.')
        ]
    )
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_is_4(self):
        self.form_data['username'] = 'Use'
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)
        msg = 'The username must have at least 4 characters.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_is_150(self):
        self.form_data['username'] = 'User' * 50
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)
        msg = 'The user must have a maximum of 4 characters.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_has_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'User'
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)
        msg = (
            'The password must have at least one uppercase letter, '
            'one lowercase letter, one number and at least 8 characters.'
        )
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = 'Jorginho@123'
        self.form_data['password2'] = 'Jorginho@456'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'The passwords do not match.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.form_data['password'] = 'Jorginho@999'
        self.form_data['password2'] = 'Jorginho@999'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'This email is already in use.'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:create')
        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password2': '@Bc123456',
        })
        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            username='testuser',
            password='@Bc123456',
        )
        self.assertTrue(is_authenticated)
