from django.test import TestCase
from .models import Label
import json
import os
from django.conf import settings
from django.contrib.auth.models import User


class LabelsCrudTestCase(TestCase):

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
                'labels',
                'fixtures',
                'labels.json'
            )
        ) as tasks_json:
            labels_fixtures_data = tasks_json.read()

        self.labels_data = json.loads(labels_fixtures_data)

    def test_create_label(self):

        response = self.client.get('/labels/create/')
        self.assertContains(response, "Label creation", status_code=200)

        response = self.client.post(
            '/labels/create/',
            {
                'name': "Test-label-4"
            },
            follow=True
        )
        self.assertContains(response, 'Label has been created successfully!', status_code=200)
        self.assertTrue(Label.objects.filter(name="Test-label-4").exists())

        response = self.client.post(
            '/labels/create/',
            {
                'name': "Test-label-1"
            },
            follow=True
        )
        self.assertContains(response, 'A label with that name already exists', status_code=400)

    def test_update_label(self):

        label_id = Label.objects.get(id=self.labels_data[0]['pk']).id
        request_url = '/label/' + str(label_id) + '/update/'

        response = self.client.post(
            request_url,
            {
                'name': "Test-label-1-edited"
            },
            follow=True
        )
        self.assertContains(response, 'Label has been updated successfully!', status_code=200)
        self.assertTrue(Label.objects.filter(name="Test-label-1-edited").exists())

    def test_delete_label(self):

        label_id = Label.objects.get(id=self.labels_data[0]['pk']).id
        request_url = '/label/' + str(label_id) + '/delete/'
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'Yes, delete', status_code=200)
        response = self.client.post(request_url, follow=True)
        self.assertContains(
            response,
            'You can not delete the Label that is assigned to the task!',
            status_code=200
        )

        status_id = Label.objects.get(id=self.labels_data[2]['pk']).id
        request_url = '/label/' + str(status_id) + '/delete/'

        response = self.client.post(request_url, follow=True)
        self.assertContains(response, 'Label has been deleted successfully!', status_code=200)

        self.assertFalse(Label.objects.filter(name=self.labels_data[2]['fields']['name']).exists())

    def test_get_all_labels(self):

        response = self.client.get('/labels/')
        self.assertContains(response, self.labels_data[0]['fields']['name'], status_code=200)
        self.assertContains(response, self.labels_data[1]['fields']['name'])
        self.assertContains(response, self.labels_data[2]['fields']['name'])
