from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from app.models import GeneralUser
from app.test.endtoendtest import EndToEndTest
from playwright.sync_api import Page
from django.db import connections

class TestMisconfig(EndToEndTest):
    
    def test_home(self):
        page = self.browser.new_page(no_viewport=True)
        def handle_response(response):
            if response.status == 404:
                self.assertEqual(response.status, 404, f"Status Code {response.status} received for /")
            elif response.status == 403:
                self.assertEqual(response.status, 403, f"Status Code {response.status} received for /")
            else:
                locator_404 = page.locator('h1:text("404")')
                self.assertTrue(locator_404.is_visible(), "404 page should be displayed for non-existent page")
        
        page.on('response', handle_response)
        page.goto(f"{self.live_server_url}/static/")

        page.close()