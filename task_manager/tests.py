from django.contrib.auth import get_user_model


class TestCaseSetUpLoginedUserMixin:
    def setUp(self):
        super().setUp()
        self.logined_user_data = {'username': 'albert_einstein',
                                  'password': 'qwer1234qwer1234'}
        self.logined_user = get_user_model().objects.create_user(
            username=self.logined_user_data['username'],
            password=self.logined_user_data['password']
        )
        self.client.login(username=self.logined_user.username,
                          password=self.logined_user_data['password'])
