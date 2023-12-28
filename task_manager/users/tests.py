from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase


def create_user(user_data):
    return get_user_model().objects.create_user(**user_data)


class TestUserSetUpMixin:
    def setUp(self):
        self.users_data = {
            'existed': {
                'username': 'albert_einstein',
                'first_name': 'Albert',
                'last_name': 'Einstein',
                'password': 'qwer1234qwer1234',
            },
            'existed_other': {
                'username': 'leonardo_da_vinci',
                'first_name': 'Leonardo',
                'last_name': 'da Vinci',
                'password': 'qwer1234qwer1234',
            },
            'new': {
                'username': 'martin_luther',
                'first_name': 'Martin',
                'last_name': 'Luther',
                'password1': 'qwer1234qwer1234',
                'password2': 'qwer1234qwer1234',
            },
            'updated': {
                'username': 'martin_luther',
                'first_name': 'Martin',
                'last_name': 'Luther King',
                'password1': 'qwer1234qwer1234',
                'password2': 'qwer1234qwer1234',
            },
        }
        self.user = create_user(self.users_data['existed'])
        self.client.login(username=self.user.username,
                          password=self.users_data['existed']['password'])


class TestUserListView(TestUserSetUpMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('user_list')

    def test_user_list_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_list_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestUserCreate(TestUserSetUpMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('user_create')

    def test_user_create_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_create_post(self):
        new_user_data = self.users_data['new']
        response = self.client.post(self.url, new_user_data)
        self.assertRedirects(response, settings.LOGIN_URL)

        created_new_user = get_user_model().objects.get(username=new_user_data['username'])
        self.assertEqual(created_new_user.username, new_user_data['username'])

    def test_user_create_page_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_create_post_not_logged_in(self):
        self.client.logout()
        new_user_data = self.users_data['new']
        response = self.client.post(self.url, new_user_data)
        self.assertRedirects(response, settings.LOGIN_URL)

        created_new_user = get_user_model().objects.get(username=new_user_data['username'])
        self.assertEqual(created_new_user.username, new_user_data['username'])


class TestUserUpdate(TestUserSetUpMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.url_self = reverse('user_update', kwargs={'pk': self.user.pk})
        self.other_user = create_user(self.users_data['existed_other'])
        self.url_other = reverse('user_update', kwargs={'pk': self.other_user.pk})

    def test_user_update_view_get_self_user(self):
        response = self.client.get(self.url_self)
        self.assertEqual(response.status_code, 200)

    def test_user_update_view_get_other_user(self):
        response = self.client.get(self.url_other)
        self.assertRedirects(response, reverse('user_list'))

    def test_user_update_view_post_self_user(self):
        updated_user_data = self.users_data['updated']
        response = self.client.post(self.url_self, updated_user_data)
        self.assertRedirects(response, reverse('user_list'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, updated_user_data['username'])

    def test_user_update_view_post_other_user(self):
        updated_user_data = self.users_data['updated']
        response = self.client.post(self.url_other, updated_user_data)
        self.assertRedirects(response, reverse('user_list'))

        self.other_user.refresh_from_db()
        self.assertNotEqual(self.other_user.username, updated_user_data['username'])

    def test_user_update_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url_self)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_user_update_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url_self, self.users_data['updated'])
        self.assertRedirects(response, settings.LOGIN_URL)

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, self.users_data['updated']['username'])


class TestUserDelete(TestUserSetUpMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.url_self = reverse('user_delete', kwargs={'pk': self.user.pk})
        self.other_user = create_user(self.users_data['existed_other'])
        self.url_other = reverse('user_delete', kwargs={'pk': self.other_user.pk})

    def test_user_delete_view_get_self_user(self):
        response = self.client.get(self.url_self)
        self.assertEqual(response.status_code, 200)

    def test_user_delete_view_get_other_user(self):
        response = self.client.get(self.url_other)
        self.assertRedirects(response, reverse('user_list'))

    def test_user_delete_view_post_self_user(self):
        response = self.client.post(self.url_self)
        self.assertRedirects(response, reverse('user_list'))

        self.assertFalse(
            get_user_model().objects.filter(pk=self.user.pk).exists(),
            'User should not exist after self-deletion'
        )

    def test_user_delete_view_post_other_user(self):
        response = self.client.post(self.url_other)
        self.assertRedirects(response, reverse('user_list'))

        self.assertTrue(
            get_user_model().objects.filter(pk=self.other_user.pk).exists(),
            'User should exist after try to deletion by other user'
        )

    def test_user_delete_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url_self)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_user_delete_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url_self)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())
