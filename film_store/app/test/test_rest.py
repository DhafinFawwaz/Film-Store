from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from app.models import GeneralUser, Film
from app.test.endtoendtest import EndToEndTest
from playwright.sync_api import Page
from django.db import connections
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
import json
from django.core.files.uploadedfile import SimpleUploadedFile
import io

class TestRest(EndToEndTest):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.seed_test_db_no_review()

      
    def convert_keys(self, film):
        film['title'] = film['name']
        film['release_year'] = film['datePublished'][0:4]

    def create_image_file(self, filename):
        image_content = io.BytesIO()
        with open(filename, "rb") as f:
            image_content.write(f.read())
        image_content.seek(0)
        return SimpleUploadedFile(filename, image_content.read(), content_type="image/jpeg")
    
    def create_video_file(self, filename):
        video_content = io.BytesIO()
        with open(filename, "rb") as f:
            video_content.write(f.read())
        video_content.seek(0)
        return SimpleUploadedFile(filename, video_content.read(), content_type="video/mp4")
      
    
    def test_login_and_get_token(self, username="admin", password="admin123"):
        login_data = {
            'username': username,
            'password': password
        }
        login_url = f"{self.live_server_url}/login"
        response = self.client.post(login_url, data=login_data, format='json')

        self.assertEqual(response.status_code, 200)
        token = response.data.get('data').get('token', None)
        self.assertIsNotNone(token)
        return token


    def test_get_all_films(self):
        token = self.test_login_and_get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        films_url = f"{self.live_server_url}/films"
        response = self.client.get(films_url)
        self.assertEqual(response.status_code, 200)
        data = response.data.get('data', None)
        self.assertIsNotNone(data)
        return data

    def assert_film_equal(self, film1: dict, film2: dict):
        self.assertEqual(film1.get('title'), film2.get('title'))
        self.assertEqual(film1.get('description'), film2.get('description'))
        self.assertEqual(film1.get('director'), film2.get('director'))
        self.assertEqual(int(film1.get('release_year')), int(film2.get('release_year')))
        self.assertEqual(float(film1.get('price')), float(film2.get('price')))
        self.assertEqual(int(film1.get('duration')), int(film2.get('duration')))

    def test_upload_film(self):

        token = self.test_login_and_get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        dataset = json.load(open("dataset/dataset.json"))
        new_film = self.find_film(dataset['films'], "The Cat with Hands")
        video_file = self.create_video_file(new_film['video'])
        cover_image = self.create_image_file(new_film['image'])
        new_film['video'] = video_file
        new_film['cover_image'] = cover_image
        self.convert_keys(new_film)

        films = self.test_get_all_films()
        self.assertEqual(len(films), 4)

        films_url = f"{self.live_server_url}/films"
        response = self.client.post(films_url, data=new_film, format='multipart')
        self.assertEqual(response.status_code, 201)
        data = response.data.get('data')
        self.assert_film_equal(data, new_film)

        films = self.test_get_all_films()
        self.assertEqual(len(films), 5)

    def test_get_film_by_id(self):
        token = self.test_login_and_get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        films = self.test_get_all_films()

        film_detail_url = f"{self.live_server_url}/films/{films[0]['id']}"
        response = self.client.get(film_detail_url)
        self.assertEqual(response.status_code, 200)
        
        data = response.data.get('data')
        self.assert_film_equal(data, films[0])


    def test_update_film(self):
        token = self.test_login_and_get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        films = self.test_get_all_films()
        film_id = films[0]['id']
        
        update_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'director': 'Updated Director',
            'release_year': '2025',
            'price': '9.99',
            'duration': '120',
        }

        film_update_url = f"{self.live_server_url}/films/{film_id}"
        response = self.client.put(film_update_url, data=update_data, format='multipart')
        self.assertEqual(response.status_code, 200)

        data = response.data.get('data')
        self.assert_film_equal(data, update_data)

    def test_delete_film(self):
        token = self.test_login_and_get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        films = self.test_get_all_films()
        print(films)
        film_id = films[0]['id']
        
        film_delete_url = f"{self.live_server_url}/films/{film_id}"

        response = self.client.get(film_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assert_film_equal(response.data.get('data'), films[0])

        response = self.client.delete(film_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assert_film_equal(response.data.get('data'), films[0])

        response = self.client.get(film_delete_url)
        self.assertEqual(response.status_code, 404)

    def test_register_user_and_get_user(self, username = "normal_user", email = "normal_user@email.com", first_name = "Normal", last_name = "User", password = "supersecretpassword123"):   
        register_data = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
        }
        register_url = f"{self.live_server_url}/register"
        response = self.client.post(register_url, data=register_data, format='json')
        self.assertEqual(response.status_code, 201)
        return response.data.get('data')
    
    def test_get_current_user(self):
        user = self.test_register_user_and_get_user()
        token = self.test_login_and_get_token(user['username'], "supersecretpassword123")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        current_user_url = f"{self.live_server_url}/self"
        response = self.client.get(current_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('data').get('username'), user['username'])
        

    def test_get_all_users(self):
        self.test_get_current_user() # will also create a user
        token = self.test_login_and_get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        users_url = f"{self.live_server_url}/users"
        response = self.client.get(users_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data.get('data'), list)
        self.assertEqual(len(response.data.get('data')), 2)

    def test_get_user_by_id(self):
        self.test_get_current_user() # will also create a user
        token = self.test_login_and_get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        users = GeneralUser.objects.all()
        for user in users:
            id = user.id
            user_detail_url = f"{self.live_server_url}/users/{id}"
            response = self.client.get(user_detail_url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.get('data').get('id'), str(id))
            self.assertEqual(response.data.get('data').get('username'), user.username)

    def test_delete_user_by_id(self):
        self.test_get_current_user() # will also create a user
        token = self.test_login_and_get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        id = GeneralUser.objects.get(username="normal_user").id
        user_detail_url = f"{self.live_server_url}/users/{id}"
        response = self.client.delete(user_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('data').get('id'), str(id))


    def test_modify_user_balance(self):
        self.test_get_current_user() # will also create a user
        token = self.test_login_and_get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        id = GeneralUser.objects.get(username="normal_user").id
        user_balance_url = f"{self.live_server_url}/users/{id}/balance"
        response = self.client.post(user_balance_url, {
            "increment": 1000
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('data').get('balance'), 1000)
        
        response = self.client.post(user_balance_url, {
            "increment": 1500
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('data').get('balance'), 2500)


    
    def test_admin_route_as_user(self):
        self.test_get_current_user() # will also create a user
        token = self.test_login_and_get_token("normal_user", "supersecretpassword123")
        print(token)

        # with no token
        for get_route in ["/users", '/users/1']:
            response = self.client.get(f"{self.live_server_url}{get_route}")
            self.assertEqual(response.status_code, 403)
        for get_route in ['films', "/films/1"]:
            response = self.client.get(f"{self.live_server_url}{get_route}")
            self.assertEqual(response.status_code, 200)

        for post_route in ["/films", "/users/1/balance"]:
            response = self.client.post(f"{self.live_server_url}{post_route}")
            self.assertEqual(response.status_code, 403)
        
        for put_route in ["/films/1"]:
            response = self.client.put(f"{self.live_server_url}{put_route}")
            self.assertEqual(response.status_code, 403)
        
        for delete_route in ["/films/1", "/users/1"]:
            response = self.client.delete(f"{self.live_server_url}{delete_route}")
            self.assertEqual(response.status_code, 403)

        # with invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        for get_route in ["/users", "/users/1"]:
            response = self.client.get(f"{self.live_server_url}{get_route}")
            self.assertEqual(response.status_code, 403)
        for get_route in ["films", "/films/1"]:
            response = self.client.get(f"{self.live_server_url}{get_route}")
            self.assertEqual(response.status_code, 200)

        for post_route in ["/films", "/users/1/balance"]:
            response = self.client.post(f"{self.live_server_url}{post_route}")
            self.assertEqual(response.status_code, 403)
        
        for put_route in ["/films/1"]:
            response = self.client.put(f"{self.live_server_url}{put_route}")
            self.assertEqual(response.status_code, 403)
        
        for delete_route in ["/films/1", "/users/1"]:
            response = self.client.delete(f"{self.live_server_url}{delete_route}")
            self.assertEqual(response.status_code, 403)
