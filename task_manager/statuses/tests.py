from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from django.test import TestCase

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tests import SetUpLoggedUserMixin


class TestStatusListView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('statuses_list')

    def test_status_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_list_view_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)


class TestStatusCreateView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_status_name = 'Test status name'
        cls.url = reverse('status_create')

    def test_status_create_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_create_view_post(self):
        response = self.client.post(self.url, {'name': self.test_status_name})
        self.assertRedirects(response, reverse('statuses_list'))

        self.assertTrue(Status.objects.filter(name=self.test_status_name).exists())

    def test_status_create_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_status_create_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url, {'name': self.test_status_name})
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertFalse(Status.objects.filter(name=self.test_status_name).exists())


class TestStatusUpdateView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_status = Status.objects.create(name='Test status')
        cls.test_status_name_to_update = 'Updated status name'
        cls.url = reverse('status_update',
                          kwargs={'pk': cls.test_status.pk})

    def test_status_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_update_view_post(self):
        response = self.client.post(
            self.url, {'name': self.test_status_name_to_update}
        )
        self.assertRedirects(response, reverse('statuses_list'))

        self.test_status.refresh_from_db()
        self.assertEqual(self.test_status.name, self.test_status_name_to_update)

    def test_status_update_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_status_update_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(
            self.url, {'name': self.test_status_name_to_update}
        )
        self.assertRedirects(response, settings.LOGIN_URL)

        self.test_status.refresh_from_db()
        self.assertNotEqual(self.test_status.name, self.test_status_name_to_update)


class TestStatusDeleteView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_status = Status.objects.create(name='Test status')
        cls.url = reverse('status_delete', kwargs={'pk': cls.test_status.pk})

    def test_status_delete_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('statuses_list'))

        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=self.test_status.pk)

    def test_status_delete_view_post_using_in_task(self):
        Task.objects.create(name='Test task',
                            status=self.test_status,
                            creator=self.logged_user)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('statuses_list'))

        self.assertTrue(Status.objects.filter(name=self.test_status.name).exists())

    def test_status_delete_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_status_delete_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertTrue(Status.objects.filter(name=self.test_status.name).exists())
