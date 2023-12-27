from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from django.test import TestCase

from task_manager.users.forms import UserCreationForm


def create_user(user_data):
    return get_user_model().objects.create_user(**user_data)


class TestUserCreate(TestCase):
    def setUp(self):
        self.users_data = {
            'new': {
                'username': 'johan',
                'first_name': 'Johan',
                'last_name': 'Weak',
                'password1': 'qwer1234qwer1234',
                'password2': 'qwer1234qwer1234',
            },
            'invalid': {
                'username': '',
                'first_name': '',
                'last_name': '',
                'password1': '123',
                'password2': '123',
            }
        }

    def test_create_user_page(self):
        url = reverse('user_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_user_form_valid(self):
        user_data = self.users_data['new']
        form = UserCreationForm(user_data)
        self.assertTrue(form.is_valid())

    def test_create_user_form_invalid(self):
        user_data = self.users_data['invalid']
        form = UserCreationForm(user_data)
        self.assertFalse(form.is_valid())

    def test_create_user_post(self):
        url = reverse('user_create')
        user_data = self.users_data['new']
        response = self.client.post(url, user_data)
        self.assertRedirects(response, settings.LOGIN_URL)

        created_new_user = get_user_model().objects.get(pk=1)
        self.assertEqual(created_new_user.username, user_data['username'])
        self.assertEqual(created_new_user.first_name, user_data['first_name'])
        self.assertEqual(created_new_user.last_name, user_data['last_name'])


class TestUserUpdate(TestCase):
    def setUp(self):
        self.users_data = {
            'initial': {
                'username': 'johan',
                'first_name': 'Johan',
                'last_name': 'Weak',
                'password': 'qwer1234qwer1234',
            },
            'updated': {
                'username': 'johan',
                'first_name': 'Johan101',
                'last_name': 'Weakness',
                'password1': 'qwer1234qwer1234qwer1234',
                'password2': 'qwer1234qwer1234qwer1234',
            },
        }

    def login(self, username, password):
        self.client.login(username=username, password=password)

    def test_update_user_page(self):
        user_data = self.users_data['initial']
        new_user = create_user(user_data)
        url = reverse('user_update', kwargs={'pk': new_user.pk})
        response = self.client.get(url)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.login(new_user.username, user_data['password'])
        updated_user_data = self.users_data['updated']
        self.client.post(url, updated_user_data)
        updated_user = get_user_model().objects.get(pk=new_user.pk)
        self.assertEqual(updated_user.username, updated_user_data['username'])
        self.assertEqual(updated_user.first_name, updated_user_data['first_name'])
        self.assertEqual(updated_user.last_name, updated_user_data['last_name'])


class TestUserDelete(TestCase):
    def setUp(self):
        self.users_data = {
            'initial': {
                'username': 'johan',
                'first_name': 'Johan',
                'last_name': 'Weak',
                'password': 'qwer1234qwer1234',
            }
        }

    def login(self, username, password):
        self.client.login(username=username, password=password)

    def test_update_user_page(self):
        user_data = self.users_data['initial']
        new_user = create_user(user_data)
        user_delete_url = reverse('user_delete', kwargs={'pk': new_user.pk})
        response = self.client.get(user_delete_url)
        self.assertRedirects(response, settings.LOGIN_URL)

        response_post = self.client.post(user_delete_url)
        self.assertRedirects(response_post, settings.LOGIN_URL)

        self.login(new_user.username, user_data['password'])
        delete_response = self.client.post(user_delete_url)
        self.assertRedirects(delete_response, reverse('user_list'))
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(pk=new_user.pk)
