from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from django.test import TestCase

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tests import SetUpLoggedUserMixin


class SetUpLoggedUserAndTestDataTaskMixin(SetUpLoggedUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_status = Status.objects.create(name='Test status')
        cls.other_user = get_user_model().objects.create(username='nelson_mandela',
                                                         password='qwer1234qwer')
        cls.test_task = Task.objects.create(name='Test task',
                                            status=cls.test_status,
                                            creator=cls.other_user)


class LoggedUserAndTestTaskDetailView(SetUpLoggedUserAndTestDataTaskMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('task_detail', kwargs={'pk': cls.test_task.pk})

    def test_task_detail_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_detail_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)


class LoggedUserAndTestTaskFilterView(SetUpLoggedUserAndTestDataTaskMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.other_status = Status.objects.create(name='Other test status')

        cls.other_user = get_user_model().objects.create(
            username='alexander_the_great', password='qwer1234qwer1234'
        )

        cls.url = reverse('tasks_list')
        cls.logged_user_task = Task.objects.create(name='Logged user task',
                                                   status=cls.other_status,
                                                   creator=cls.logged_user)

    def test_task_filter_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(list(response.context['tasks']), Task.objects.all())

    def test_task_filter_view_get_by_status(self):
        filter_param_test_status = {'status': self.test_status.pk}
        response = self.client.get(self.url, filter_param_test_status)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['tasks'],
            Task.objects.filter(**filter_param_test_status)
        )

    def test_task_filter_view_get_by_executor(self):
        self.test_task.executor = self.logged_user
        self.test_task.save()

        filter_param_executor = {'executor': self.logged_user.pk}
        response = self.client.get(self.url, filter_param_executor)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['tasks'],
            Task.objects.filter(**filter_param_executor)
        )

    def test_task_filter_view_get_by_label(self):
        test_label = Label.objects.create(name='Test label')
        self.test_task.labels.set([test_label])

        filter_param_label = {'label': test_label.pk}
        response = self.client.get(self.url, filter_param_label)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['tasks'],
            Task.objects.filter(labels__in=[test_label])
        )

    def test_task_filter_view_get_by_own_tasks(self):
        filter_param_own_tasks = {'own_tasks': 'on'}
        response = self.client.get(self.url, filter_param_own_tasks)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['tasks'], [self.logged_user_task])

    def test_status_filter_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)


class LoggedUserAndTestTaskCreateView(SetUpLoggedUserAndTestDataTaskMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data_to_create_task = {
            'name': 'Test task to create',
            'status': cls.test_status.pk,
            'creator': cls.other_user.pk
        }
        cls.url = reverse('task_create')

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


class LoggedUserAndTestTaskUpdateView(SetUpLoggedUserAndTestDataTaskMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data_to_update_task = {
            'name': 'Test task to update',
            'status': cls.test_status.pk,
            'description': 'Some description'
        }
        cls.url = reverse('task_update', kwargs={'pk': cls.test_task.pk})

    def test_task_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_update_view_post(self):
        response = self.client.post(self.url, self.data_to_update_task)
        self.assertRedirects(response, reverse('tasks_list'))

        self.test_task.refresh_from_db()
        self.assertEqual(self.test_task.name, self.data_to_update_task['name'])
        self.assertEqual(self.test_task.description, self.data_to_update_task['description'])

    def test_task_update_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_task_update_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url, self.data_to_update_task)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.test_task.refresh_from_db()
        self.assertNotEqual(self.test_task.name, self.data_to_update_task['name'])


class LoggedUserAndTestTaskDeleteView(SetUpLoggedUserAndTestDataTaskMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url_other = reverse('task_delete', kwargs={'pk': cls.test_task.pk})
        cls.logged_user_task = Task.objects.create(name='Logged user task',
                                                   status=cls.test_status,
                                                   creator=cls.logged_user)
        cls.url_own = reverse('task_delete', kwargs={'pk': cls.logged_user_task.pk})

    def test_task_delete_view_get(self):
        response = self.client.get(self.url_own)
        self.assertEqual(response.status_code, 200)

    def test_task_delete_view_post(self):
        response = self.client.post(self.url_own)
        self.assertRedirects(response, reverse('tasks_list'))

        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=self.logged_user_task.pk)

    def test_task_delete_view_post_other_user(self):
        response = self.client.post(self.url_other)
        self.assertRedirects(response, reverse('tasks_list'))

        self.assertTrue(
            Task.objects.filter(pk=self.test_task.pk).exists(),
            'Task should not be deleted by other user'
        )

    def test_task_delete_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url_own)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_task_delete_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url_own)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertTrue(Task.objects.filter(pk=self.logged_user_task.pk).exists())
