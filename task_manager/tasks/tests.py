from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TestSetUpDataAndLoginUserMixin:
    @classmethod
    def setUpTestData(cls):
        cls.users_data = {
            'logined_user': {'username': 'michelangelo', 'password': 'qwer1234qwer1234'}

        }
        cls.user = get_user_model().objects.create_user(
            username=cls.users_data['logined_user']['username'],
            password=cls.users_data['logined_user']['password'])

        cls.status_initial = Status.objects.create(name='Initial status')
        cls.status_updated = Status.objects.create(name='Updated status')
        cls.test_data = {
            'create': {
                'name': 'Task to create',
                'status': cls.status_initial.pk,
            },
            'update': {
                'name': 'Updated task',
                'description': 'Task after update',
                'status': cls.status_updated.pk,
                'executor': cls.user.pk,
            },
            'created': {
                'name': 'Created task',
                'status': cls.status_updated,
                'creator': cls.user,
            },
        }
        cls.created_task = Task.objects.create(**cls.test_data['created'])

    def setUp(self):
        self.client.login(username=self.user.username,
                          password=self.users_data['logined_user']['password'])


class TestTaskListView(TestSetUpDataAndLoginUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('tasks_list')

    def test_task_list_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_list_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)


class TestTaskCreateView(TestSetUpDataAndLoginUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('task_create')

    def test_task_create_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_create_view_post(self):
        task_data = self.test_data['create']
        response = self.client.post(self.url, task_data)
        self.assertRedirects(response, reverse('tasks_list'))

        self.assertTrue(Task.objects.filter(name=task_data['name']).exists())

    def test_task_create_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_status_create_view_post_not_logged_in(self):
        self.client.logout()
        task_data = self.test_data['create']
        response = self.client.post(self.url, task_data)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertFalse(Task.objects.filter(name=task_data['name']).exists())


class TestTaskUpdateView(TestSetUpDataAndLoginUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('task_update', kwargs={'pk': self.created_task.pk})

    def test_task_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_update_view_post(self):
        task_update_data = self.test_data['update']
        response = self.client.post(self.url, task_update_data)
        self.assertRedirects(response, reverse('tasks_list'))

        self.created_task.refresh_from_db()
        self.assertEqual(self.created_task.name, task_update_data['name'])

    def test_task_update_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_task_update_view_post_not_logged_in(self):
        self.client.logout()
        task_update_data = self.test_data['update']
        response = self.client.post(self.url, task_update_data)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.created_task.refresh_from_db()
        self.assertNotEqual(self.created_task.name, task_update_data['name'])


class TestTaskDeleteView(TestSetUpDataAndLoginUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('task_delete', kwargs={'pk': self.created_task.pk})

    def test_task_delete_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('tasks_list'))

        self.assertFalse(Task.objects.filter(pk=self.created_task.pk).exists())

    def test_task_delete_view_post_other_user(self):
        other_user = get_user_model().objects.create(username='other_user',
                                                     password='qwer1234qwer1234')
        other_user_task = Task.objects.create(name='Other user task',
                                              status=self.status_initial,
                                              creator=other_user)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('tasks_list'))

        self.assertTrue(
            Task.objects.filter(pk=other_user_task.pk).exists(),
            'Task should not be deleted by other user'
        )

    def test_task_delete_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_task_delete_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertTrue(Task.objects.filter(pk=self.created_task.pk).exists())
