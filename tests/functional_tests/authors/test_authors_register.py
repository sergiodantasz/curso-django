from pytest import mark
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.authors.base import AuthorsBaseTest


@mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')
        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Ex.: David')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The first name cannot be empty.', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex.: Anton')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The last name cannot be empty.', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Ex.: DavidAnton_123')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The username cannot be empty.', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Type your password here.')
            password2 = self.get_by_placeholder(form, 'Re-enter your password here.')
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Different')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The passwords do not match.', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.get_by_placeholder(form, 'Ex.: David').send_keys('First Name')
        self.get_by_placeholder(form, 'Ex.: Anton').send_keys('Last Name')
        self.get_by_placeholder(form, 'Ex.: DavidAnton_123').send_keys('my_username')
        self.get_by_placeholder(form, 'Ex.: davidanton@email.com').send_keys('email@valid.com')
        self.get_by_placeholder(form, 'Type your password here.').send_keys('P@ssw0rd1')
        self.get_by_placeholder(form, 'Re-enter your password here.').send_keys('P@ssw0rd1')
        form.submit()
        self.assertIn(
            'Your user has been created successfully, please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
