from django.test import TestCase
from .models import Task
import json
import os
from django.conf import settings
from django.contrib.auth.models import User


class TasksCrudTestCase(TestCase):

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

        with open(
            os.path.join(
                settings.BASE_DIR,
                'task_manager',
                'tasks',
                'fixtures',
                'tasks.json'
            )
        ) as tasks_json:
            tasks_fixtures_data = tasks_json.read()

        self.tasks_data = json.loads(tasks_fixtures_data)

        self.client.login(
            username=self.users_data[1]['fields']['username'],
            password=self.users_data[1]['fields']['password']
        )

    def test_create_task(self):

        response = self.client.get('/tasks/create/')
        self.assertContains(response, "Task creation", status_code=200)

        response = self.client.post(
            '/tasks/create/',
            {
                'name': "Test-task-3",
                'description': 'Test descriptrion',
                'status': 1,
                'executor': 2,
            },
            follow=True
        )
        self.assertContains(response, 'Task has been created successfully!', status_code=200)
        self.assertTrue(Task.objects.filter(name="Test-task-3").exists())

        response = self.client.post(
            '/tasks/create/',
            {
                'name': "Test-task-1",
                'description': 'Test descriptrion',
                'status': 1,
                'executor': 2
            },
            follow=True
        )
        self.assertContains(response, 'A task with that name already exists', status_code=400)

    def test_update_task(self):

        task_id = Task.objects.get(id=self.tasks_data[0]['pk']).id
        request_url = '/task/' + str(task_id) + '/update/'


        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'Only author of the task can edit it!', status_code=200)
        
        task_id = Task.objects.get(id=self.tasks_data[1]['pk']).id
        request_url = '/task/' + str(task_id) + '/update/'

        response = self.client.post(
            request_url,
            {
                'name': "Test-task-1-edited",
                'description': 'Test descriptrion',
                'status': 1,
                'executor': 2,
                'labels': [1, 2]
            },
            follow=True
        )
        self.assertContains(response, 'Task has been updated successfully!', status_code=200)
        self.assertTrue(Task.objects.filter(name="Test-task-1-edited").exists())

        self.client.login(
            username=self.users_data[0]['fields']['username'],
            password=self.users_data[0]['fields']['password']
        )

        response = self.client.post(  # test what admin can edit any task
            request_url,
            {
                'name': "Test-task-1-edited-2",
                'description': 'Test descriptrion',
                'status': 1,
                'executor': 2
            },
            follow=True
        )

        self.assertContains(response, 'Task has been updated successfully!', status_code=200)
        self.assertTrue(Task.objects.filter(name="Test-task-1-edited-2").exists())

    def test_delete_task(self):

        task_id = Task.objects.get(id=self.tasks_data[0]['pk']).id
        request_url = '/task/' + str(task_id) + '/delete/'
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'Only author of the task can delete it!', status_code=200)
        response = self.client.post(request_url, follow=True)
        self.assertContains(response, 'Only author of the task can delete it!', status_code=200)


        task_id = Task.objects.get(id=self.tasks_data[1]['pk']).id
        request_url = '/task/' + str(task_id) + '/delete/'

        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'Yes, delete', status_code=200)
        response = self.client.post(request_url, follow=True)
        self.assertContains(response, 'Task has been deleted successfully!', status_code=200)

        self.assertFalse(Task.objects.filter(name=self.tasks_data[1]['fields']['name']).exists())

    def test_delete_task_admin(self):
        '''Test what admin can delete any task'''
        self.client.login(
            username=self.users_data[0]['fields']['username'],
            password=self.users_data[0]['fields']['password']
        )

        task_id = Task.objects.get(id=self.tasks_data[1]['pk']).id
        request_url = '/task/' + str(task_id) + '/delete/'

        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'Yes, delete', status_code=200)
        response = self.client.post(request_url, follow=True)
        self.assertContains(response, 'Task has been deleted successfully!', status_code=200)

        self.assertFalse(Task.objects.filter(name=self.tasks_data[1]['fields']['name']).exists())


    def test_get_all_tasks(self):

        response = self.client.get('/tasks/')
        self.assertContains(response, self.tasks_data[0]['fields']['name'], status_code=200)
        self.assertContains(response, self.tasks_data[1]['fields']['name'])
