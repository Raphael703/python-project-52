from django.contrib.auth import get_user_model


class TestCaseSetUpLoggedUserMixin:
    def setUp(self):
        self.logged_user_data = {'username': 'albert_einstein',
                                 'password': 'qwer1234qwer1234'}
        self.logged_user = get_user_model().objects.create_user(
            username=self.logged_user_data['username'],
            password=self.logged_user_data['password']
        )
        self.client.login(username=self.logged_user.username,
                          password=self.logged_user_data['password'])
