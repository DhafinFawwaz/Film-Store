import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from app.models import GeneralUser
from app.test.endtoendtest import EndToEndTest
from playwright.sync_api import Page
from django.db import connections

class TestLogin(EndToEndTest):
    def setUp(cls):
        GeneralUser.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@email.com',
        )


    def test_admin(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/signin")
        page.fill('[name=username]', 'admin')
        page.fill('[name=password]', 'admin123')
        page.click('[value=Login]')
        self.assertEqual(page.url, f"{self.live_server_url}/", f"Admin should be able to login with correct username and password")
        self.simulate_logout(page)
        page.close()


    def test_normal_user(self):
        page = self.browser.new_page()
        self.simulate_register_normal_user(page)
        page.goto(f"{self.live_server_url}/signin")
        page.fill('[name=username]', 'normal_user')
        page.fill('[name=password]', 'Supersecretpassword123')
        page.click('[value=Login]')
        self.assertEqual(page.url, f"{self.live_server_url}/", f"User should be able to login with correct username and password")
        self.simulate_logout(page)
        page.close()

    def test_nonexistentuser(self):
        page = self.browser.new_page()
        self.simulate_register_normal_user(page)
        page.goto(f"{self.live_server_url}/signin")
        page.fill('[name=username]', 'nonexistentuser')
        page.fill('[name=password]', 'nonexistentpassword')
        page.click('[value=Login]')
        self.assertEqual(page.url, f"{self.live_server_url}/signin", f"Non-existent user should not be able to login")
        page.close()

    def test_wrongpassword(self):
        page = self.browser.new_page()
        self.simulate_register_normal_user(page)
        page.goto(f"{self.live_server_url}/signin")
        page.fill('[name=username]', 'normal_user')
        page.fill('[name=password]', 'wrongpassword')
        page.click('[value=Login]')
        self.assertEqual(page.url, f"{self.live_server_url}/signin", f"User should not be able to login with wrong password")
        page.close()
