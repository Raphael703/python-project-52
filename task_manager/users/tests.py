from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase


def create_user(user_data):
    return get_user_model().objects.create_user(**user_data)


class TestSetUpMixin:
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
        self.existed_user_data = self.users_data['existed']
        self.user = create_user(self.existed_user_data)
        self.client.login(username=self.user.username,
                          password=self.existed_user_data['password'])
        self.url = reverse('user_create')


class TestUserListView(TestSetUpMixin, TestCase):

    def test_user_list_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_list_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestUserCreate(TestSetUpMixin, TestCase):

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
        response = self.client.post(self.url, self.users_data['new'])
        self.assertRedirects(response, settings.LOGIN_URL)


class TestUserUpdate(TestSetUpMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.url_self = reverse('user_update', kwargs={'pk': self.user.pk})
        self.url_other = reverse('user_update', kwargs={'pk': create_user(self.users_data['existed_other']).pk})

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

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_user_data['username'])

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


class TestUserDelete(TestSetUpMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.url_self = reverse('user_delete', kwargs={'pk': self.user.pk})
        self.url_other = reverse('user_delete', kwargs={'pk': create_user(self.users_data['existed_other']).pk})

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
            get_user_model().objects.filter(pk=self.user.pk).exists(),
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
