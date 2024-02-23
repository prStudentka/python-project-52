from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.users.models import CustomUser
from task_manager.users.forms import RegistrationForm
from django.core.exceptions import ObjectDoesNotExist


# Create your tests here.
class UserCrudTest(TestCase):

    def setUp(self):
        self.test_user = CustomUser.objects.create_user(
            first_name='Blue',
            last_name='Joe',
            username='user_test1',
            password='12345'
        )
        self.login_data = {
            'username': 'user_test1',
            'password': '12345'
        }

    def test_open_registration(self):
        url = reverse_lazy('create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, template_name='form.html')
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        form_data = {
            'first_name': 'Petrov',
            'last_name': 'Ivan',
            'username': 'user_test',
            'password1': 'abcd',
            'password2': 'abcd'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_user(self):
        data = {
            'first_name': 'Petrov',
            'last_name': 'Ivan',
            'username': 'user_test',
            'password1': 'abcd',
            'password2': 'abcd'
        }
        url = reverse_lazy('create')
        response = self.client.post(url, data, format='json')
        self.assertRedirects(response, reverse_lazy('log in'), status_code=302)
        user = CustomUser.objects.get(username=data['username'])
        self.assertEqual(user.first_name, data['first_name'])

    def test_login_user(self):
        url = reverse_lazy('log in')
        self.client.login(username=self.login_data['username'], password=self.login_data['password'])
        response = self.client.post(url, self.login_data)
        self.assertRedirects(response, reverse_lazy('index'), status_code=302)

    def test_update_user(self):
        update_data = {
            'first_name': 'Ivanov',
            'last_name': 'Ivan',
            'username': 'user_test',
            'password1': 'abcd',
            'password2': 'abcd'
        }
        self.client.login(username=self.login_data['username'], password=self.login_data['password'])
        url = reverse_lazy('update', args=[self.test_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data=update_data)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.first_name, update_data['first_name'])
        self.assertRedirects(response, reverse_lazy('users_index'), status_code=302)

    def test_delete_user(self):
        self.client.force_login(user=self.test_user)
        before_count_users = len(CustomUser.objects.all())
        self.assertEqual(before_count_users, 1)
        key = self.test_user.pk
        url = reverse_lazy('delete', kwargs={'pk': key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(url)
        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(pk=key)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users_index'))
