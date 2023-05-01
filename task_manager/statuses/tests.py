from django.test import TestCase
from .models import Status
import json
import os
from django.conf import settings
from django.contrib.auth.models import User


class StatusCrudTestCase(TestCase):

    fixtures = ["users", "statuses", "labels", "tasks"]

    def setUp(self):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
        
        with open(
            os.path.join(
                settings.BASE_DIR,
                'task_manager',
                'users',
                'fixtures',
                'users.json'
            )
        ) as users_json:
            users_fixtures_data = users_json.read()

        self.users_data = json.loads(users_fixtures_data)

        self.client.login(
            username=self.users_data[1]['fields']['username'],
            password=self.users_data[1]['fields']['password']
        )

        with open(
            os.path.join(
                settings.BASE_DIR,
                'task_manager',
                'statuses',
                'fixtures',
                'statuses.json'
            )
        ) as tasks_json:
            statuses_fixtures_data = tasks_json.read()

        self.statuses_data = json.loads(statuses_fixtures_data)

    def test_create_status(self):

        response = self.client.get('/status/create/')
        self.assertContains(response, "Status creation", status_code=200)

        response = self.client.post(
            '/status/create/',
            {
                'name': "Test-status-4"
            },
            follow=True
        )
        self.assertContains(response, 'Status has been created successfully!', status_code=200)
        self.assertTrue(Status.objects.filter(name="Test-status-4").exists())

        response = self.client.post(
            '/status/create/',
            {
                'name': "Test-status-1"
            },
            follow=True
        )
        self.assertContains(response, 'A status with that name already exists', status_code=400)

    def test_update_status(self):

        status_id = Status.objects.get(id=self.statuses_data[0]['pk']).id
        request_url = '/status/' + str(status_id) + '/update/'

        response = self.client.post(
            request_url,
            {
                'name': "Test-status-1-edited"
            },
            follow=True
        )
        self.assertContains(response, 'Status has been updated successfully!', status_code=200)
        self.assertTrue(Status.objects.filter(name="Test-status-1-edited").exists())

    def test_delete_status(self):

        status_id = Status.objects.get(id=self.statuses_data[0]['pk']).id
        request_url = '/status/' + str(status_id) + '/delete/'
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'Yes, delete', status_code=200)
        response = self.client.post(request_url, follow=True)
        self.assertContains(response, 'You can not delete the status that is assigned to the task!', status_code=200)

        status_id = Status.objects.get(id=self.statuses_data[2]['pk']).id
        request_url = '/status/' + str(status_id) + '/delete/'

        response = self.client.post(request_url, follow=True)
        self.assertContains(response, 'Status has been deleted successfully!', status_code=200)

        self.assertFalse(Status.objects.filter(name=self.statuses_data[2]['fields']['name']).exists())

    def test_get_all_tasks(self):

        response = self.client.get('/statuses/')
        self.assertContains(response, self.statuses_data[0]['fields']['name'], status_code=200)
        self.assertContains(response, self.statuses_data[1]['fields']['name'])
        self.assertContains(response, self.statuses_data[2]['fields']['name'])
