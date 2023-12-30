from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class SetUpLoggedUserMixin:
    def setUp(self):
        self.logged_user_data = {'username': 'albert_einstein',
                                 'password': 'qwer1234qwer1234'}
        self.logged_user = get_user_model().objects.create_user(
            username=self.logged_user_data['username'],
            password=self.logged_user_data['password']
        )
        self.client.login(username=self.logged_user.username,
                          password=self.logged_user_data['password'])


class TestIndexTemplateView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('index')

    def test_index_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestUserLoginView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('login')

    def test_user_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_login_view_post(self):
        self.client.logout()
        response = self.client.post(self.url, self.logged_user_data)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.logged_user.pk)


class TestUserLogoutView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('logout')

    def test_user_logout_view_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('index'))


class TestNotFoundedPage(TestCase):
    def test_not_founded_page(self):
        response = self.client.get('/not-founded-page/')
        self.assertEqual(response.status_code, 404)
