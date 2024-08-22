
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from app.models import GeneralUser, Film, Review
from app.test.endtoendtest import EndToEndTest
from playwright.sync_api import Page
from django.db import connections
from app.api.seed.seed import seed_db
import json

class TestFilm(EndToEndTest):

    def find_film(arr, name):
        for film in arr:
            if film["name"] == name:
                return film

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        dataset = json.load(open("dataset/dataset.json"))
        selected_films = ["The Batman", "No Time to Die", "Mauri", "Ek Doctor Ki Maut"]

        film_to_remove = []
        for film in dataset['films']:
            if film["name"] not in selected_films:
                film_to_remove.append(film)
        for film in film_to_remove:
            dataset['films'].remove(film)
        

        the_batman = TestFilm.find_film(dataset['films'], "The Batman")
        no_time_to_die = TestFilm.find_film(dataset['films'], "No Time to Die")
        mauri = TestFilm.find_film(dataset['films'], "Mauri")
        ek_doctor_ki_maut = TestFilm.find_film(dataset['films'], "Ek Doctor Ki Maut")
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
    
    

    # def test_details_review_access(self):
    #     page = self.browser.new_page()

    #     films = Film.objects.all()
    #     for film in films:
    #         page.goto(f"{self.live_server_url}/details/{film.id}")
    #         self.assertEqual(page.url, f"{self.live_server_url}/details/{film.id}", f"Any User should be able to access all film details page")
    #         page.goto(f"{self.live_server_url}/details/{film.id}/review")
    #         self.assertEqual(page.url, f"{self.live_server_url}/details/{film.id}/review", f"Any User should be able to access all film review page")
    #     page.close()

    #     # manual
    #     page = self.browser.new_page()
    #     page.goto(f"{self.live_server_url}")
    #     for film in films:
    #         page.click(f'text="{film.title}"')
    #         self.assertEqual(page.url, f"{self.live_server_url}/details/{film.id}", f"Authenticated User should be able to access all film details page")
    #         review_button = page.locator('text="See More Review"')
    #         if not review_button.is_visible(): 
    #             page.click('text="Back"')
    #             self.assertEqual(page.url, f"{self.live_server_url}/explore", f"Authenticated User should be able to go back to home page")
    #             continue

    #         page.click(f'text="See More Review"')
    #         self.assertEqual(page.url, f"{self.live_server_url}/details/{film.id}/review", f"Authenticated User should be able to access all film review page")
    #         page.click('text="Back"')
    #         self.assertEqual(page.url, f"{self.live_server_url}/details/{film.id}", f"Authenticated User should be able to go back to details page")
    #         page.click('text="Back"')
    #         self.assertEqual(page.url, f"{self.live_server_url}/explore", f"Authenticated User should be able to go back to home page")
    #     page.close()

    # def test_wishlist(self):
    #     page = self.browser.new_page()

    #     films = Film.objects.all()

    #     for film in films:
    #         page.goto(f"{self.live_server_url}/explore")
    #         page.click(f'text="{film.title}"')
    #         self.assertEqual(page.url, f"{self.live_server_url}/details/{film.id}", f"Any User should be able to access all film details page")
    #         page.click('text="Login To Buy"')
    #         self.assertEqual(page.url, f"{self.live_server_url}/signin", f"Not Authenticated User should not be able to add film to wishlist")

    #     self.simulate_register(page)
    #     self.simulate_login(page)

    #     page.click('text="The Batman"')
    #     page.click(f'button:has(div:text("Wishlist"))')
    #     page.wait_for_timeout(1000)
    #     unwishlist_locator = page.locator('text="Unwishlist"')
    #     self.assertTrue(unwishlist_locator.is_visible())
    #     page.click('text=Back')
        
    #     page.click('text="No Time to Die"')
    #     page.click(f'button:has(div:text("Wishlist"))')
    #     unwishlist_locator = page.locator('text="Unwishlist"')
    #     page.click('text="Back"')

    #     page.click('text="Mauri"')
    #     page.click(f'button:has(div:text("Wishlist"))')
    #     unwishlist_locator = page.locator('text="Unwishlist"')
    #     page.click('text="Back"')

    #     self.simulate_click_nav(page, "/wishlist")

    #     self.assertEqual(page.url, f"{self.live_server_url}/wishlist", f"Authenticated User should be able to access wishlist page")

    #     the_batman_locator = page.locator('div:text("The Batman")')
    #     no_time_to_die_locator = page.locator('div:text("No Time to Die")')
    #     mauri_locator = page.locator('div:text("Mauri")')
    #     ek_doctor_ki_maut_locator = page.locator('div:text("Ek Doctor Ki Maut")')

    #     self.assertTrue(the_batman_locator.is_visible())
    #     self.assertTrue(no_time_to_die_locator.is_visible())
    #     self.assertTrue(mauri_locator.is_visible())
    #     self.assertFalse(ek_doctor_ki_maut_locator.is_visible())

    #     self.simulate_click_nav(page, "/")

    #     page.click('text="The Batman"')
    #     page.click('text="Unwishlist"')
    #     page.click('text="Back"')

    #     page.click('text="No Time to Die"')
    #     page.click('text="Unwishlist"')

    #     self.simulate_click_nav(page, "/wishlist")

    #     self.assertEqual(page.url, f"{self.live_server_url}/wishlist", f"Authenticated User should be able to access wishlist page")

    #     the_batman_locator = page.locator('div:text("The Batman")')
    #     no_time_to_die_locator = page.locator('div:text("No Time to Die")')
    #     mauri_locator = page.locator('div:text("Mauri")')
    #     ek_doctor_ki_maut_locator = page.locator('div:text("Ek Doctor Ki Maut")')

    #     self.assertFalse(the_batman_locator.is_visible())
    #     self.assertFalse(no_time_to_die_locator.is_visible())
    #     self.assertTrue(mauri_locator.is_visible())
    #     self.assertFalse(ek_doctor_ki_maut_locator.is_visible())

    #     page.click('text="Mauri"')
    #     page.click('text="Unwishlist"')

    #     self.simulate_click_nav(page, "/wishlist")

    #     the_batman_locator = page.locator('div:text("The Batman")')
    #     no_time_to_die_locator = page.locator('div:text("No Time to Die")')
    #     mauri_locator = page.locator('div:text("Mauri")')
    #     ek_doctor_ki_maut_locator = page.locator('div:text("Ek Doctor Ki Maut")')

    #     self.assertFalse(the_batman_locator.is_visible())
    #     self.assertFalse(no_time_to_die_locator.is_visible())
    #     self.assertFalse(mauri_locator.is_visible())
    #     self.assertFalse(ek_doctor_ki_maut_locator.is_visible())



    #     page.close()

    # def test_search(self):
    #     page = self.browser.new_page()

    #     self.simulate_register(page)
    #     self.simulate_login(page)

    #     self.assertEqual(page.url, f"{self.live_server_url}/", f"Authenticated User should be able to access home page")

    #     page.fill('#search', 'au')
    #     page.press('#search', 'Enter')

    #     self.assertEqual(page.url, f"{self.live_server_url}/explore?q=au", f"Authenticated User should be able to search for films")
        

    #     the_batman_locator = page.locator('div:text("The Batman")')
    #     no_time_to_die_locator = page.locator('div:text("No Time to Die")')
    #     mauri_locator = page.locator('div:text("Mauri")')
    #     ek_doctor_ki_maut_locator = page.locator('div:text("Ek Doctor Ki Maut")')
    #     self.assertFalse(the_batman_locator.is_visible())
    #     self.assertFalse(no_time_to_die_locator.is_visible())
    #     self.assertTrue(mauri_locator.is_visible())
    #     self.assertTrue(ek_doctor_ki_maut_locator.is_visible())
    #     page.close()

    # make 4 people rating, check the average rating
    # make review with other people, then view it with another people, then review it by self, then review again by self, there should be only one review
    # make review with <script> tag injection
    # TODO: test all rest api access, also test rest api and make sure only admin can access with the correct token

    def set_balance(self, page: Page, balance: int, username="normal_user"):
        GeneralUser.objects.filter(username=username).update(balance=balance)
        # TODO: change this with rest api

    def test_purchase(self):
        page = self.browser.new_page()

        self.simulate_register(page)
        self.simulate_login(page)

        self.set_balance(page, 5500)
        page.goto(f"{self.live_server_url}/explore")
        
        page.click('text="Ek Doctor Ki Maut"')
        page.click(f'button:has(div:text("Purchase"))')
        page.wait_for_timeout(200)
        button = page.locator("button[type='submit']:has-text('Purchase')")
        self.assertTrue(button.is_enabled())
        page.wait_for_timeout(200)
        page.click(f'#dialog-cancel-button')
        page.click('text="Back"')

        page.click('text="Mauri"')
        page.click(f'button:has(div:text("Purchase"))')
        page.wait_for_timeout(200)
        button = page.locator("button[type='submit']:has-text('Purchase')")
        self.assertTrue(button.is_enabled())
        button.click()
        page.wait_for_timeout(200)
        balance_text = int(page.locator("#user-balance-absolute").text_content())
        self.assertEqual(balance_text, 2500, "User should be able to purchase a film")
        page.click('text="Back"')

        page.click('text="No Time to Die"')
        page.click(f'button:has(div:text("Purchase"))')
        page.wait_for_timeout(200)
        button = page.locator("button[type='submit']:has-text('Purchase')")
        self.assertTrue(button.is_enabled())
        button.click()
        page.wait_for_timeout(200)
        balance_text = int(page.locator("#user-balance-absolute").text_content())
        self.assertEqual(balance_text, 500, "User should be able to purchase a film")
        page.click('text="Back"')

        page.click('text="The Batman"')
        page.click(f'button:has(div:text("Purchase"))')
        page.wait_for_timeout(200)
        button = page.locator("button[type='submit']:has-text('Purchase')")
        self.assertTrue(button.is_disabled())
        page.wait_for_timeout(200)
        page.click(f'#dialog-cancel-button')
        page.click('text="Back"')


        self.simulate_click_nav(page, "/bought")

        the_batman_locator = page.locator('div:text("The Batman")')
        no_time_to_die_locator = page.locator('div:text("No Time to Die")')
        mauri_locator = page.locator('div:text("Mauri")')
        ek_doctor_ki_maut_locator = page.locator('div:text("Ek Doctor Ki Maut")')

        self.assertFalse(the_batman_locator.is_visible())
        self.assertTrue(no_time_to_die_locator.is_visible())
        self.assertTrue(mauri_locator.is_visible())
        self.assertFalse(ek_doctor_ki_maut_locator.is_visible())

        page.click('text="No Time to Die"')
        page.click('text="Watch"')
        no_time_to_die = Film.objects.get(title="No Time to Die")
        self.assertEqual(page.url, f"{self.live_server_url}/details/{no_time_to_die.id}/watch", f"Authenticated User should be able to watch a film")
        page.click('text="Back"')

        page.click('text="Mauri"')
        page.click('text="Watch"')
        mauri = Film.objects.get(title="Mauri")
        self.assertEqual(page.url, f"{self.live_server_url}/details/{mauri.id}/watch", f"Authenticated User should be able to watch a film")

        the_batman = Film.objects.get(title="The Batman")
        page.goto(f"{self.live_server_url}/details/{the_batman.id}/watch")
        self.assertEqual(page.url, f"{self.live_server_url}/details/{the_batman.id}", f"Unpurchased film should not be able to be watched")

        ek_docktor_ki_maut = Film.objects.get(title="Ek Doctor Ki Maut")
        page.goto(f"{self.live_server_url}/details/{ek_docktor_ki_maut.id}/watch")
        self.assertEqual(page.url, f"{self.live_server_url}/details/{ek_docktor_ki_maut.id}", f"Unpurchased film should not be able to be watched")

    def test_rating(self):
        pass
