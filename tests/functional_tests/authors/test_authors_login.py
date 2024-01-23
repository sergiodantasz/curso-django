from django.contrib.auth.models import User
from django.urls import reverse
from pytest import mark
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.authors.base import AuthorsBaseTest


@mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        password_value = 'password'
        user = User.objects.create_user(username='test_user', password=password_value)
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username.')
        password_field = self.get_by_placeholder(form, 'Type your password.')
        username_field.send_keys(user.username)
        password_field.send_keys(password_value)
        form.submit()
        self.assertIn(
            f'You are logged in as {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_form_is_invalid(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username.')
        password_field = self.get_by_placeholder(form, 'Type your password.')
        username_field.send_keys(' ')
        password_field.send_keys(' ')
        form.submit()
        self.assertIn(
            'Username or password is invalid.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_invalid_credentials(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username.')
        password_field = self.get_by_placeholder(form, 'Type your password.')
        username_field.send_keys('invalid_user')
        password_field.send_keys('invalid_password')
        form.submit()
        self.assertIn(
            'Username or password is invalid.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
