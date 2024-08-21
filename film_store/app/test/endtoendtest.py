import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from django.db import connections
from playwright.sync_api import Page

class EndToEndTest(StaticLiveServerTestCase):
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless= not int(os.environ.get("TEST_HEAD", 1)))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()
        connections.close_all()


    def simulate_logout(self, page: Page):
        page.hover('#nav-button')
        page.wait_for_timeout(100) # ensure dropdown to appear
        page.click('button:has(div:text("Logout"))')
        self.assertEqual(page.url, f"{self.live_server_url}/signin", f"User should be able to logout")

    def simulate_register_normal_user(self, page: Page):
        page.goto(f"{self.live_server_url}/signup")
        self.assertEqual(page.url, f"{self.live_server_url}/signup", f"User should be logged out before registering")
        page.fill('[name=username]', 'normal_user')
        page.fill('[name=email]', 'normal_user@email.com')
        page.fill('[name=first_name]', 'Normal')
        page.fill('[name=last_name]', 'User')
        page.fill('[name=password1]', 'Supersecretpassword123')
        page.fill('[name=password2]', 'Supersecretpassword123')
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signin", "normal_user should be able to register")