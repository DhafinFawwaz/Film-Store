from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from app.models import GeneralUser
from app.test.endtoendtest import EndToEndTest
from playwright.sync_api import Page
from django.db import connections

class TestLogin(EndToEndTest):

    def test_register_with_existing_username(self):
        page = self.browser.new_page()
        self.simulate_register(page)
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'normal_user')  # Existing username
        page.fill('[name=email]', 'new_email@email.com')
        page.fill('[name=first_name]', 'New')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', 'supersecretpassword123')
        page.fill('[name=password2]', 'supersecretpassword123')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with an existing username")
        page.close()

    def test_register_with_existing_email(self):
        page = self.browser.new_page()
        self.simulate_register(page)
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'new_user')
        page.fill('[name=email]', 'normal_user@email.com')  # Existing email
        page.fill('[name=first_name]', 'New')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', 'supersecretpassword123')
        page.fill('[name=password2]', 'supersecretpassword123')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with an existing email")
        page.close()

    def test_register_with_empty_username(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=email]', 'new_user@email.com')
        page.fill('[name=first_name]', 'New')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', 'supersecretpassword123')
        page.fill('[name=password2]', 'supersecretpassword123')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with an empty username")
        page.close()

    def test_register_with_empty_email(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'new_user')
        page.fill('[name=first_name]', 'New')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', 'supersecretpassword123')
        page.fill('[name=password2]', 'supersecretpassword123')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with an empty email")
        page.close()

    def test_register_with_empty_first_name(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'new_user')
        page.fill('[name=email]', 'new_user@email.com')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', 'supersecretpassword123')
        page.fill('[name=password2]', 'supersecretpassword123')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with an empty first name")
        page.close()

    def test_register_with_empty_last_name(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'new_user')
        page.fill('[name=email]', 'new_user@email.com')
        page.fill('[name=first_name]', 'New')
        page.fill('[name=password1]', 'supersecretpassword123')
        page.fill('[name=password2]', 'supersecretpassword123')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with an empty last name")
        page.close()

    def test_register_with_empty_password1(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'new_user')
        page.fill('[name=email]', 'new_user@email.com')
        page.fill('[name=first_name]', 'New')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password2]', 'supersecretpassword123')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with an empty password")
        page.close()

    def test_register_with_empty_password2(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'new_user')
        page.fill('[name=email]', 'new_user@email.com')
        page.fill('[name=first_name]', 'New')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', 'supersecretpassword123')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with an empty password confirmation")
        page.close()

    def test_register_with_short_password(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'new_user')
        page.fill('[name=email]', 'new_user@email.com')
        page.fill('[name=first_name]', 'New')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', 'short')
        page.fill('[name=password2]', 'short')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with a short password")
        page.close()

    def test_register_with_no_digit_in_password(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'new_user')
        page.fill('[name=email]', 'new_user@email.com')
        page.fill('[name=first_name]', 'New')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', 'NoDigitsHere')
        page.fill('[name=password2]', 'NoDigitsHere')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with a password that has no digits")
        page.close()

    def test_register_with_no_letter_in_password(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'new_user')
        page.fill('[name=email]', 'new_user@email.com')
        page.fill('[name=first_name]', 'New')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', '123456789')
        page.fill('[name=password2]', '123456789')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with a password that has no digits")
        page.close()


    def test_register_with_non_matching_passwords(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signup")
        page.fill('[name=username]', 'new_user')
        page.fill('[name=email]', 'new_user@email.com')
        page.fill('[name=first_name]', 'New')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', 'supersecretpassword123')
        page.fill('[name=password2]', 'Differentpassword123')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signup", "User should not be able to register with non-matching passwords")
        page.close()