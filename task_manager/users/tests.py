from django.test import TestCase
import json
import os
from django.conf import settings
from django.contrib.auth.models import User


class UserCrudTestCase(TestCase):

    fixtures = ["users"]

    def setUp(self):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

        with open(os.path.join(
            settings.BASE_DIR,
            'task_manager',
            'users',
            'fixtures',
            'users.json'
        )) as users_json:
            users_fixtures_data = users_json.read()

        self.users_data = json.loads(users_fixtures_data)

    def test_create_user(self):

        response = self.client.get('/users/create/')
        self.assertContains(response, "Registration", status_code=200)

        response = self.client.post(
            '/users/create/',
            {
                'username': "Testuser2",
                'first_name': "Test",
                'last_name': "User",
                'password1': "33Test1122!",
                'password2': "33Test1122!",
            },
            follow=True
        )
        self.assertContains(response, 'User has been registered successfully!', status_code=200)
        self.assertTrue(User.objects.filter(username="Testuser2").exists())

        response = self.client.post(
            '/users/create/',
            {
                'username': self.users_data[0]['fields']['username'],
                'first_name': "Test",
                'last_name': "User",
                'password1': "33Test1122!",
                'password2': "33Test1122!",
            },
            follow=True
        )
        self.assertContains(response, 'A user with that username already exists', status_code=400)

        response = self.client.post(
            '/users/create/',
            {
                'username': "!!!**(*^^)",
                'first_name': "Tset",
                'last_name': "User",
                'password1': "33Test1122!",
                'password2': "33Test1122!!!",
            },
            follow=True
        )
        self.assertContains(response, 'The two password fields didn’t match.', status_code=400)
        self.assertContains(
            response,
            'only letters, numbers, and @/./+/-/_ characters.',
            status_code=400
        )

        response = self.client.post(
            '/users/create/',
            {
                'username': "Testuser3",
                'first_name': "Test",
                'last_name': "User",
                'password1': "123",
                'password2': "123",
            },
            follow=True
        )
        self.assertContains(
            response,
            'This password is too short. It must contain at least 8 characters',
            status_code=400
        )
        self.assertContains(response, 'This password is too common.', status_code=400)
        self.assertContains(response, 'his password is entirely numeric.', status_code=400)

    def test_login(self):

        response = self.client.post(
            '/login/',
            {
                'username': self.users_data[0]['fields']['username'],
                'password': "12321323"
            }
        )
        self.assertContains(response, "Invalid username or password", status_code=400)

        response = self.client.get('/login/')
        self.assertContains(response, "Login", status_code=200)

        response = self.client.post(
            '/login/',
            {
                'username': self.users_data[0]['fields']['username'],
                'password': self.users_data[0]['fields']['password'],
            },
            follow=True
        )
        self.assertContains(response, "Logout", status_code=200)

        response = self.client.post(
            '/login/',
            {
                'username': self.users_data[0]['fields']['username'],
                'password': self.users_data[0]['fields']['password'],
            },
            follow=False
        )
        self.assertEqual(response.status_code, 302)

    def test_update_user(self):

        user_id = User.objects.get(id=self.users_data[0]['pk']).id
        request_url = '/users/' + str(user_id) + '/update/'

        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'You are not authorized, please log in!', status_code=200)

        self.client.login(
            username=self.users_data[1]['fields']['username'],
            password=self.users_data[1]['fields']['password']
        )
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'You have no permission to edit users!', status_code=200)

        user_id = User.objects.get(id=self.users_data[1]['pk']).id
        request_url = '/users/' + str(user_id) + '/update/'

        response = self.client.post(
            request_url,
            {
                'username': "Testuser2edit",
                'first_name': "Test-edit",
                'last_name': "User-edit",
                'password1': "33Test1122!edit",
                'password2': "33Test1122!edit",
            },
            follow=True
        )
        self.assertContains(response, 'User has been updated successfully!', status_code=200)
        self.assertFalse(User.objects.filter(username="Testuser2").exists())

        self.client.login(
            username=self.users_data[0]['fields']['username'],
            password=self.users_data[0]['fields']['password']
        )

        response = self.client.post(
            request_url,
            {
                'username': "Testuser2edit2",
                'first_name': "Test-edit2",
                'last_name': "User-edit2",
                'password1': "33Test1122!edit2",
                'password2': "33Test1122!edit2",
            },
            follow=True
        )

        self.assertContains(response, 'User has been updated successfully!', status_code=200)
        self.assertFalse(User.objects.filter(username="Testuser2edit").exists())

    def test_delete_user(self):

        user_id = User.objects.get(id=self.users_data[1]['pk']).id
        request_url = '/users/' + str(user_id) + '/delete/'
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'You are not authorized, please log in!', status_code=200)

        self.client.login(
            username=self.users_data[1]['fields']['username'],
            password=self.users_data[1]['fields']['password']
        )
        response = self.client.post(request_url, follow=True)
        self.assertContains(response, 'You can not delete yourself!', status_code=200)

        user_2_id = User.objects.get(id=self.users_data[0]['pk']).id
        request_url_2 = '/users/' + str(user_2_id) + '/delete/'
        response = self.client.post(request_url_2, follow=True)
        self.assertContains(response, 'You have no permission to delete users!', status_code=200)

        self.client.login(
            username=self.users_data[0]['fields']['username'],
            password=self.users_data[0]['fields']['password']
        )
        response = self.client.post(request_url, {}, follow=True)
        self.assertContains(response, 'User has been deleted successfully!', status_code=200)

    def test_get_all_users(self):

        response = self.client.get('/users/')
        self.assertContains(response, self.users_data[0]['fields']['username'], status_code=200)
        self.assertContains(response, self.users_data[1]['fields']['username'])
