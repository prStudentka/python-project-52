from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.users.models import CustomUser
from task_manager.users.forms import RegistrationForm
from django.core.exceptions import ObjectDoesNotExist
from task_manager.views import IndexView
from django.core.management import call_command


# Create your tests here.
class UserCrudTest(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        call_command('loaddata', 'users.json', verbosity=2)
        self.test_user = CustomUser.objects.get(pk=1)
        self.data = {
            'first_name': 'Petrov',
            'last_name': 'Ivan',
            'username': 'user_test',
            'password1': 'abcd',
            'password2': 'abcd'
        }

    def test_homepage(self):
        response = self.client.get('/', headers={"accept-language": "ru"})
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, IndexView)
        self.assertIn(response.context['button'], 'Узнать больше')

    def test_open_registration(self):
        url = reverse_lazy('create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, template_name='users/create.html')
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        form = RegistrationForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_create_user(self):
        url = reverse_lazy('create')
        response = self.client.post(url, self.data, format='json')
        self.assertRedirects(response, reverse_lazy('log in'), status_code=302)
        user = CustomUser.objects.get(username=self.data['username'])
        self.assertEqual(user.first_name, self.data['first_name'])

    def test_login_user(self):
        new_password = '12345'
        self.test_user.set_password(new_password)
        self.test_user.save()
        login_data = {
            'username': self.test_user.username,
            'password': new_password
        }
        url = reverse_lazy('log in')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, login_data, follow=True)
        url_back = reverse_lazy('index')
        self.assertRedirects(response, url_back, status_code=302)
        self.assertTemplateUsed(response, template_name='index.html')

    def test_update_user(self):
        self.client.force_login(user=self.test_user)
        url = reverse_lazy('update', args=[self.test_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data=self.data)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.first_name, self.data['first_name'])
        url_back = reverse_lazy('users_index')
        self.assertRedirects(response, url_back, status_code=302)

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
