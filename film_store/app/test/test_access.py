from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from app.models import GeneralUser
from app.test.endtoendtest import EndToEndTest
from playwright.sync_api import Page
from django.db import connections

class TestAccess(EndToEndTest):
    
    def test_home(self):
        page = self.browser.new_page()

        self.simulate_register(page)
        self.simulate_login(page)

        self.simulate_click_nav(page, "/")
        self.assertEqual(page.url, f"{self.live_server_url}/", f"Authenticated User should be able to access home page by navigation buttons")

        page.goto(f"{self.live_server_url}/")
        self.assertEqual(page.url, f"{self.live_server_url}/", f"Authenticated User should be able to access home page")
        
        self.simulate_logout(page)
        page.close()

    def test_profile(self):
        page = self.browser.new_page()

        page.goto(f"{self.live_server_url}/profile")
        self.assertEqual(page.url, f"{self.live_server_url}/signin", f"Unauthenticated User should be redirected to signin page")

        self.simulate_register(page)
        self.simulate_login(page)

        self.simulate_click_nav(page, "/profile")
        self.assertEqual(page.url, f"{self.live_server_url}/profile", f"Authenticated User should be able to access profile page by navigation buttons")

        page.goto(f"{self.live_server_url}/profile")
        self.assertEqual(page.url, f"{self.live_server_url}/profile", f"Authenticated User should be able to access profile page directly")
        
        self.simulate_logout(page)
        page.close()

    def test_bought(self):
        page = self.browser.new_page()

        page.goto(f"{self.live_server_url}/bought")
        self.assertEqual(page.url, f"{self.live_server_url}/signin", f"Unauthenticated User should be redirected to signin page")

        self.simulate_register(page)
        self.simulate_login(page)

        self.simulate_click_nav(page, "/bought")
        self.assertEqual(page.url, f"{self.live_server_url}/bought", f"Authenticated User should be able to access bought page by navigation buttons")

        page.goto(f"{self.live_server_url}/bought")
        self.assertEqual(page.url, f"{self.live_server_url}/bought", f"Authenticated User should be able to access bought page directly")
        
        self.simulate_logout(page)
        page.close()

    def test_wishlist(self):
        page = self.browser.new_page()

        page.goto(f"{self.live_server_url}/wishlist")
        self.assertEqual(page.url, f"{self.live_server_url}/signin", f"Unauthenticated User should be redirected to signin page")

        self.simulate_register(page)
        self.simulate_login(page)

        self.simulate_click_nav(page, "/wishlist")
        self.assertEqual(page.url, f"{self.live_server_url}/wishlist", f"Authenticated User should be able to access wishlist page by navigation buttons")

        page.goto(f"{self.live_server_url}/wishlist")
        self.assertEqual(page.url, f"{self.live_server_url}/wishlist", f"Authenticated User should be able to access wishlist page directly")
        
        self.simulate_logout(page)
        page.close()

    def test_logout(self):
        page = self.browser.new_page()
        self.simulate_register(page)
        self.simulate_login(page)

        self.simulate_logout(page)
        page.close()

    def test_signin(self):
        page = self.browser.new_page()

        self.simulate_register(page)
        self.simulate_login(page)
        page.goto(f"{self.live_server_url}/signin")
        self.assertEqual(page.url, f"{self.live_server_url}/", f"Authenticated User should not be able to access signin page")
        page.close()

    def test_signup(self):
        page = self.browser.new_page()

        self.simulate_register(page)
        self.simulate_login(page)
        page.goto(f"{self.live_server_url}/signup")
        self.assertEqual(page.url, f"{self.live_server_url}/", f"Authenticated User should not be able to access signup page")
        page.close()

    
