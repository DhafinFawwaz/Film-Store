
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from app.models import GeneralUser
from app.test.endtoendtest import EndToEndTest
from playwright.sync_api import Page
from django.db import connections
from app.api.seed.seed import seed_db
import json

class TestFilm(EndToEndTest):

    def find_film(self, arr, name):
        for film in arr:
            if film["name"] == name:
                return film

    def setUp(self):
        super().setUp()
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
        

        review_to_remove = []
        for review in dataset['review']:
            if review["film"] not in selected_films:
                review_to_remove.append(review)
        for review in review_to_remove:
            dataset['review'].remove(review)

        for user in dataset['user']:
            bought_films = user['bought']
            wishlist_films = user['wishlist']
            user['bought'] = [film for film in bought_films if film in selected_films]
            user['wishlist'] = [film for film in wishlist_films if film in selected_films]

        seed_db(dataset)
    
    # test access to details, reviews, watch
    # test wishlist, unwishlist
    # test search "au"
    # test purchase
    # test purchase not enough balance, check balance still the same
    # test purchase already bought
    # make review with <script>

    def test_search(self):
        page = self.browser.new_page()

        self.simulate_register(page)
        self.simulate_login(page)

        self.assertEqual(page.url, f"{self.live_server_url}/", f"Authenticated User should be able to access home page")

        page.fill('#search', 'au')
        page.press('#search', 'Enter')

        self.assertEqual(page.url, f"{self.live_server_url}/explore?q=au", f"Authenticated User should be able to search for films")
        
        search_results = page.query_selector_all('.film-card')
        self.assertEqual(len(search_results), 2, "Search results should be correct")

        mauri_locator = page.locator('div:text("Mauri")')
        ek_doctor_ki_maut_locator = page.locator('div:text("Ek Doctor Ki Maut")')
        self.assertTrue(mauri_locator.is_visible())
        self.assertTrue(ek_doctor_ki_maut_locator.is_visible())

        
        self.simulate_logout(page)
        page.close()

