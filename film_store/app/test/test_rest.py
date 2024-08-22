from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from app.models import GeneralUser
from app.test.endtoendtest import EndToEndTest
from playwright.sync_api import Page
from django.db import connections

class TestAccess(EndToEndTest):
    
    def test_rest(self):
        pass