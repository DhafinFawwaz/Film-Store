import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from django.db import connections
from playwright.sync_api import Page
from app.models import GeneralUser
from django.core.cache import cache
from app.api.seed.seed import seed_db
import json
from io import StringIO
import sys

class EndToEndTest(StaticLiveServerTestCase):
    serialized_rollback = True
    _original_stdout = None

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless= not int(os.environ.get("TEST_HEAD", 1)), args=["--start-maximized"])
        cls.browser.new_context(no_viewport=True)
        # EndToEndTest._original_stdout = sys.stdout
        # sys.stdout = StringIO()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()
        connections.close_all()
        cache.clear()

        # sys.stdout = EndToEndTest._original_stdout

    def setUp(self):
        cache.clear()
        GeneralUser.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@email.com',
        )

    def tearDown(self):
        cache.clear()
    

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


    def find_film(self, arr, name):
        for film in arr:
            if film["name"] == name:
                return film
            
    def seed_test_db_no_review(self):
        dataset = json.load(open("dataset/dataset.json"))
        selected_films = ["The Batman", "No Time to Die", "Mauri", "Ek Doctor Ki Maut"]

        film_to_remove = []
        for film in dataset['films']:
            if film["name"] not in selected_films:
                film_to_remove.append(film)
        for film in film_to_remove:
            dataset['films'].remove(film)
        

        the_batman = self.find_film(dataset['films'], "The Batman")
        no_time_to_die = self.find_film(dataset['films'], "No Time to Die")
        mauri = self.find_film(dataset['films'], "Mauri")
        ek_doctor_ki_maut = self.find_film(dataset['films'], "Ek Doctor Ki Maut")
        the_batman['price'] = 1000
        no_time_to_die['price'] = 2000
        mauri['price'] = 3000
        ek_doctor_ki_maut['price'] = 4000
        

        dataset['user'] = []
        dataset['review'] = []
        seed_db(dataset)
    