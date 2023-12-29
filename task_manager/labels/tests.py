from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from django.test import TestCase

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tests import TestCaseSetUpLoginedUserMixin


class TestLabelListView(TestCaseSetUpLoginedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('labels_list')

    def test_label_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_label_list_view_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)


class TestLabelCreateView(TestCaseSetUpLoginedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_label_name = 'Test label name'
        cls.url = reverse('label_create')

    def test_label_create_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_label_create_view_post(self):
        response = self.client.post(self.url, {'name': self.test_label_name})
        self.assertRedirects(response, reverse('labels_list'))

        self.assertTrue(Label.objects.filter(name=self.test_label_name).exists())

    def test_label_create_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_label_create_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url, {'name': self.test_label_name})
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertFalse(Label.objects.filter(name=self.test_label_name).exists())


class TestLabelUpdateView(TestCaseSetUpLoginedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_label = Label.objects.create(name='Test label')
        cls.test_label_name_to_update = 'Updated label name'
        cls.url = reverse('label_update',
                          kwargs={'pk': cls.test_label.pk})

    def test_label_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_label_update_view_post(self):
        response = self.client.post(
            self.url, {'name': self.test_label_name_to_update}
        )
        self.assertRedirects(response, reverse('labels_list'))

        self.test_label.refresh_from_db()
        self.assertEqual(self.test_label.name, self.test_label_name_to_update)

    def test_label_update_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_label_update_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(
            self.url, {'name': self.test_label_name_to_update}
        )
        self.assertRedirects(response, settings.LOGIN_URL)

        self.test_label.refresh_from_db()
        self.assertNotEqual(self.test_label.name, self.test_label_name_to_update)


class TestLabelDeleteView(TestCaseSetUpLoginedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_label = Label.objects.create(name='Test label')
        cls.url = reverse('label_delete', kwargs={'pk': cls.test_label.pk})

    def test_label_delete_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_label_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('labels_list'))

        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=self.test_label.pk)

    def test_label_delete_view_post_using_in_task(self):
        task = Task.objects.create(
            name='Test task',
            status=Status.objects.create(name='Test status'),
            creator=self.logined_user)
        task.labels.set([self.test_label])

        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('labels_list'))

        self.assertTrue(Label.objects.filter(name=self.test_label.name).exists())

    def test_label_delete_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

    def test_label_delete_view_post_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, settings.LOGIN_URL)

        self.assertTrue(Label.objects.filter(name=self.test_label.name).exists())
