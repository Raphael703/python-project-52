from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from django.test import TestCase

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tests import SetUpLoggedUserMixin


class TestUserListView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('user_list')

    def test_user_list_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_list_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestUserCreate(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data_to_create_user = {
            'username': 'albert_einstein',
            'password1': 'qwer1234qwer1234',
            'password2': 'qwer1234qwer1234'
        }
        cls.url = reverse('user_create')

    def test_user_create_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_create_post(self):
        response = self.client.post(self.url, self.data_to_create_user)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertTrue(get_user_model().objects.filter(
            username=self.data_to_create_user['username']).exists())


class TestUserUpdate(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.other_user_data = {
            'username': 'confucius',
            'password': 'qwer1234qwer1234',
        }
        cls.user_data_to_update = {
            'username': 'updated_username',
            'first_name': 'Michel',
            'last_name': 'Angelo',
            'password1': 'qwer1234qwer1234',
            'password2': 'qwer1234qwer1234',
        }
        cls.other_user = get_user_model().objects.create(**cls.other_user_data)
        cls.url_self = reverse('user_update', kwargs={'pk': cls.logged_user.pk})
        cls.url_other = reverse('user_update', kwargs={'pk': cls.other_user.pk})

    def test_user_update_view_get_self_user(self):
        response = self.client.get(self.url_self)
        self.assertEqual(response.status_code, 200)

    def test_user_update_view_get_other_user(self):
        response = self.client.get(self.url_other)
        self.assertRedirects(response, reverse('user_list'))

    def test_user_update_view_post_self_user(self):
        response = self.client.post(self.url_self, self.user_data_to_update)
        self.assertRedirects(response, reverse('user_list'))

        self.logged_user.refresh_from_db()
        self.assertEqual(self.logged_user.username, self.user_data_to_update['username'])
        self.assertEqual(self.logged_user.first_name, self.user_data_to_update['first_name'])
        self.assertEqual(self.logged_user.last_name, self.user_data_to_update['last_name'])

    def test_user_update_view_post_other_user(self):
        self.user_data_to_update['username'] = 'try_to_update_username'
        response = self.client.post(self.url_other, self.user_data_to_update)
        self.assertRedirects(response, reverse('user_list'))

        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.username, self.other_user_data['username'])
        self.assertNotEqual(self.other_user.first_name, self.user_data_to_update['first_name'])
        self.assertNotEqual(self.other_user.last_name, self.user_data_to_update['last_name'])

    def test_user_update_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url_self)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_user_update_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url_self, self.user_data_to_update)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.logged_user.refresh_from_db()
        self.assertNotEqual(self.logged_user.username, self.user_data_to_update['username'])


class TestUserDelete(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.other_user_data = {
            'username': 'confucius',
            'password': 'qwer1234qwer1234',
        }
        cls.other_user = get_user_model().objects.create(**cls.other_user_data)
        cls.url_self = reverse('user_delete', kwargs={'pk': cls.logged_user.pk})
        cls.url_other = reverse('user_delete', kwargs={'pk': cls.other_user.pk})

    def test_user_delete_view_get_self_user(self):
        response = self.client.get(self.url_self)
        self.assertEqual(response.status_code, 200)

    def test_user_delete_view_get_other_user(self):
        response = self.client.get(self.url_other)
        self.assertRedirects(response, reverse('user_list'))

    def test_user_delete_view_post_self_user(self):
        response = self.client.post(self.url_self)
        self.assertRedirects(response, reverse('user_list'))

        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(pk=self.logged_user.pk)

    def test_user_delete_view_post_self_user_created_task(self):
        test_status = Status.objects.create(name='Test test_status for task')
        Task.objects.create(
            name='Test task', status=test_status, creator=self.logged_user
        )
        response = self.client.post(self.url_self)
        self.assertRedirects(response, reverse('user_list'))

        self.assertTrue(
            get_user_model().objects.filter(pk=self.logged_user.pk).exists(),
            'User should not be deleted if he is associated with task as creator'
        )
        Task.objects.create(
            name='Test task, executor - logged_user', status=test_status,
            creator=self.other_user, executor=self.logged_user
        )
        response = self.client.post(self.url_self)
        self.assertRedirects(response, reverse('user_list'))

        self.assertTrue(
            get_user_model().objects.filter(pk=self.logged_user.pk).exists(),
            'User should not be deleted if he is associated with task as executor'
        )

    def test_user_delete_view_post_other_user(self):
        response = self.client.post(self.url_other)
        self.assertRedirects(response, reverse('user_list'))

        self.assertTrue(
            get_user_model().objects.filter(pk=self.other_user.pk).exists(),
            'User cannot be deleted by another user'
        )

    def test_user_delete_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url_self)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_user_delete_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url_self)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertTrue(get_user_model().objects.filter(pk=self.logged_user.pk).exists())
