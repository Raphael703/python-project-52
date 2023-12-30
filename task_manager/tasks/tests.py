from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tests import SetUpLoggedUserMixin


class TestTaskDetailView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_status = Status.objects.create(name='Test status')

    def setUp(self):
        super().setUp()
        self.test_task = Task.objects.create(name='Test task',
                                             status=self.test_status,
                                             creator=self.logged_user)
        self.url = reverse('task_detail', kwargs={'pk': self.test_task.pk})

    def test_task_detail_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_detail_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)


class TestTaskFilterView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_status = Status.objects.create(name='Test status')
        cls.other_status = Status.objects.create(name='Other test status')

        cls.other_user = get_user_model().objects.create(
            username='alexander_the_great', password='qwer1234qwer1234'
        )
        cls.other_user_task1 = Task.objects.create(name='Other user task1',
                                                   status=cls.test_status,
                                                   creator=cls.other_user)
        cls.other_user_task2 = Task.objects.create(name='Other user task2',
                                                   status=cls.other_status,
                                                   creator=cls.other_user)

        cls.url = reverse('tasks_list')

    def test_task_filter_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(list(response.context['tasks']), Task.objects.all())

    def test_task_filter_view_get_by_status(self):
        filter_params_test_status = {'status': self.test_status.pk}
        response = self.client.get(self.url, filter_params_test_status)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['tasks'],
            Task.objects.filter(**filter_params_test_status)
        )

    def test_task_filter_view_get_by_executor(self):
        self.other_user_task1.executor = self.logged_user

        filter_params_executor = {'status': self.logged_user.pk}
        response = self.client.get(self.url, filter_params_executor)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['tasks'],
            Task.objects.filter(**filter_params_executor)
        )

    def test_task_filter_view_get_by_label(self):
        label = Label.objects.create(name='Test label')
        self.other_user_task1.labels.set([label])

        filter_params_label = {'status': label.pk}
        response = self.client.get(self.url, filter_params_label)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['tasks'],
            Task.objects.filter(**filter_params_label)
        )

    def test_task_filter_view_get_by_own_tasks(self):
        filter_params_label = {'own_tasks': 'on'}

        own_task = Task.objects.create(name='Own task',
                                       status=self.test_status,
                                       creator=self.logged_user)
        response = self.client.get(self.url, filter_params_label)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['tasks'], [own_task])

    def test_status_filter_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)


class TestTaskCreateView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_status = Status.objects.create(name='Test status')

    def setUp(self):
        super().setUp()
        self.data_to_create_task = {
            'name': 'Test task to create',
            'status': self.test_status.pk,
            'creator': self.logged_user.pk
        }
        self.url = reverse('task_create')

    def test_task_create_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_create_view_post(self):
        response = self.client.post(self.url, self.data_to_create_task)
        self.assertRedirects(response, reverse('tasks_list'))

        self.assertTrue(Task.objects.filter(name=self.data_to_create_task['name']).exists())

    def test_task_create_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_status_create_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url, self.data_to_create_task)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertFalse(Task.objects.filter(name=self.data_to_create_task).exists())


class TestTaskUpdateView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_status = Status.objects.create(name='Test status')
        cls.data_to_update_task = {
            'name': 'Test task to update',
            'status': cls.test_status.pk,
            'description': 'Some description'
        }

    def setUp(self):
        super().setUp()
        self.test_task = Task.objects.create(name='Test task',
                                             status=self.test_status,
                                             creator=self.logged_user)
        self.url = reverse('task_update', kwargs={'pk': self.test_task.pk})

    def test_task_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_update_view_post(self):
        response = self.client.post(self.url, self.data_to_update_task)
        self.assertRedirects(response, reverse('tasks_list'))

        self.test_task.refresh_from_db()
        self.assertEqual(self.test_task.name, self.data_to_update_task['name'])
        self.assertEqual(self.test_task.description,
                         self.data_to_update_task['description'])

    def test_task_update_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_task_update_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url, self.data_to_update_task)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.test_task.refresh_from_db()
        self.assertNotEqual(self.test_task.name,
                            self.data_to_update_task['name'])


class TestTaskDeleteView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_status = Status.objects.create(name='Test status')
        cls.other_user = get_user_model().objects.create(
            username='alexander_the_great', password='qwer1234qwer1234'
        )
        cls.other_user_task = Task.objects.create(name='Other user task',
                                                  status=cls.test_status,
                                                  creator=cls.other_user)

    def setUp(self):
        super().setUp()
        self.test_task = Task.objects.create(name='Test task',
                                             status=self.test_status,
                                             creator=self.logged_user)
        self.url = reverse('task_delete', kwargs={'pk': self.test_task.pk})

    def test_task_delete_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('tasks_list'))

        self.assertFalse(Task.objects.filter(pk=self.test_task.pk).exists())

    def test_task_delete_view_post_other_user(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('tasks_list'))

        self.assertTrue(
            Task.objects.filter(pk=self.other_user_task.pk).exists(),
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

        self.assertTrue(Task.objects.filter(pk=self.test_task.pk).exists())
