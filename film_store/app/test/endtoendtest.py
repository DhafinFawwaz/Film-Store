import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from django.db import connections
from playwright.sync_api import Page
from app.models import GeneralUser
from django.core.cache import cache

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
        cache.clear()

    def setUp(self):
        cache.clear()
        GeneralUser.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@email.com',
        )

    def simulate_click_nav(self, page: Page, href: str):
        page.hover('#nav-button')
        page.wait_for_timeout(100) # ensure dropdown to appear
        page.click(f'a[href="{href}"]')
        self.assertEqual(page.url, f"{self.live_server_url}{href}", f"User should be able to navigate to {href}")

    def simulate_logout(self, page: Page):
        page.hover('#nav-button')
        page.wait_for_timeout(100) # ensure dropdown to appear
        page.click(f'button:has(div:text("Logout"))')
        self.assertEqual(page.url, f"{self.live_server_url}/signin", f"User should be able to logout")


    def simulate_login(self, page: Page, username = "normal_user", password = "supersecretpassword123"):
        page.goto(f"{self.live_server_url}/signin")
        self.assertEqual(page.url, f"{self.live_server_url}/signin", f"User should be logged out before logging in")
        page.fill('[name=username]', username)
        page.fill('[name=password]', password)
        page.click('[value=Login]')
        self.assertEqual(page.url, f"{self.live_server_url}/", f"User should be able to login")

    def simulate_register(self, page: Page, username = "normal_user", email = "normal_user@email.com", first_name = "Normal", last_name = "User", password = "supersecretpassword123"):
        page.goto(f"{self.live_server_url}/signup")
        self.assertEqual(page.url, f"{self.live_server_url}/signup", f"User should be logged out before registering")
        page.fill('[name=username]', username)
        page.fill('[name=email]', email)
        page.fill('[name=first_name]', first_name)
        page.fill('[name=last_name]', last_name)
        page.fill('[name=password1]', password)
        page.fill('[name=password2]', password)
        page.click('[value=Register]')
        self.assertEqual(page.url, f"{self.live_server_url}/signin", "normal_user should be able to register")


    def login_admin_rest() -> dict:
        return ""