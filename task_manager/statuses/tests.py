from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from django.test import TestCase

from task_manager.statuses.models import Status
from task_manager.users.tests import create_user

test_user_data = {
    'username': 'Abraham',
    'password': 'qwer1234qwer1234'
}


def create_status(name):
    return Status.objects.create(name=name)


class TestStatusListView(TestCase):
    def setUp(self):
        self.user = create_user(test_user_data)
        self.client.login(
            username=self.user.username, password=test_user_data['password'])
        self.url = reverse('statuses_list')

    def test_status_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_list_view_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)


class TestStatusCreateView(TestCase):
    def setUp(self):
        self.user = create_user(test_user_data)
        self.client.login(
            username=self.user.username, password=test_user_data['password'])
        self.url = reverse('status_create')

    def test_status_create_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_create_view_post(self):
        test_status_name = 'test_status'
        response = self.client.post(self.url, {'name': test_status_name})
        self.assertRedirects(response, reverse('statuses_list'))

        status = Status.objects.get(name=test_status_name)
        self.assertEqual(status.name, test_status_name)

    def test_status_create_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_status_create_view_post_not_logged_in(self):
        self.client.logout()
        test_status_name = 'Try status'
        response = self.client.post(self.url, {'name': test_status_name})
        self.assertRedirects(response, settings.LOGIN_URL)

        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(name=test_status_name)


class TestStatusUpdateView(TestCase):
    def setUp(self):
        self.test_status = create_status('Test status to update')
        self.user = create_user(test_user_data)
        self.client.login(
            username=self.user.username, password=test_user_data['password'])
        self.url = reverse('status_update', kwargs={'pk': self.test_status.pk})

    def test_status_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_update_view_post(self):
        test_status_name = 'updated status name'
        response = self.client.post(self.url, {'name': test_status_name})
        self.assertRedirects(response, reverse('statuses_list'))

        status = Status.objects.get(name=test_status_name)
        self.assertEqual(status.name, test_status_name)

    def test_status_update_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_status_update_view_post_not_logged_in(self):
        self.client.logout()
        test_status_name = 'try update status'
        response = self.client.post(self.url, {'name': test_status_name})
        self.assertRedirects(response, settings.LOGIN_URL)

        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(name=test_status_name)


class TestStatusDeleteView(TestCase):
    def setUp(self):
        self.test_status = create_status('Test status to delete')
        self.user = create_user(test_user_data)
        self.client.login(
            username=self.user.username, password=test_user_data['password'])
        self.url = reverse('status_delete', kwargs={'pk': self.test_status.pk})

    def test_status_delete_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('statuses_list'))

        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=self.test_status.pk)

    def test_status_delete_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_status_delete_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

        status = Status.objects.get(pk=self.test_status.pk)
        self.assertEqual(status.name, self.test_status.name)
