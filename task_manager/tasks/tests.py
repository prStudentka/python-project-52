from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from task_manager.tasks.filters import TaskFilter


# Create your tests here.
class TaskCrudTest(TestCase):

    def setUp(self):
        self.test_author = CustomUser.objects.create_user(
            first_name='Blue',
            last_name='Joe',
            username='user_test1',
            password='12345'
        )
        self.executor = CustomUser.objects.create_user(
            first_name='Pizza',
            last_name='Delivery',
            username='user_test',
            password='12345'
        )
        self.status = Status.objects.create(name='status_test')
        self.label1 = Label.objects.create(name='label test one')
        self.first_task = Task.objects.create(
            name='Task first',
            description='first description',
            status=self.status,
            executor=self.executor,
            author=self.test_author
        )
        self.first_task.labels.add(self.label1)
        self.login_data = {
            'username': 'user_test1',
            'password': '12345'
        }

    def test_create_task(self):
        data = {
            'name': 'Task test',
            'description': 'test description',
            'status': self.status.pk,
            'executor': self.executor.pk,
            'author': self.test_author.pk
        }
        url = reverse_lazy('create task')
        self.client.login(username=self.login_data['username'],
                          password=self.login_data['password'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data, format='json')
        url_back = reverse_lazy('tasks_index')
        self.assertRedirects(response, url_back, status_code=302)
        task_name = Task.objects.get(name=data['name'])
        self.assertEqual(task_name.name, data['name'])

    def test_update_task(self):
        update_data = {
            'name': 'Task update test',
            'description': 'test description',
            'status': self.status.pk,
            'author': self.test_author.pk
        }
        self.client.login(username=self.login_data['username'],
                          password=self.login_data['password'])
        url = reverse_lazy('update task', args=[self.first_task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data=update_data)
        self.first_task.refresh_from_db()
        self.assertEqual(self.first_task.name, update_data['name'])
        url_back = reverse_lazy('tasks_index')
        self.assertRedirects(response, url_back, status_code=302)

    def test_delete_task(self):
        self.client.force_login(user=self.test_author)
        key = self.first_task.pk
        url = reverse_lazy('delete task', kwargs={'pk': key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(url)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=key)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_index'))

    def test_fail_delete_task_another_user(self):
        self.client.force_login(user=self.executor)
        key = self.first_task.pk
        url = reverse_lazy('delete task', kwargs={'pk': key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertRaisesMessage(
            expected_exception=PermissionDenied,
            expected_message='Only author of the task can delete it'
        )
        self.assertEqual(response.status_code, 302)

    def test_detail_task(self):
        self.client.force_login(user=self.test_author)
        key = self.first_task.pk
        url = reverse_lazy('detail task', args=[key])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='task.html')

    def test_filter_task(self):
        data = {
            'status': self.status,
        }
        self.status1 = Status.objects.create(name='status and test ')
        self.client.force_login(user=self.test_author)
        url = reverse_lazy('tasks_index')
        tasks = Task.objects.all()
        response = self.client.get(url)
        filter_queryset = TaskFilter(data, tasks, request=response).qs
        self.assertIn(self.first_task, filter_queryset)

    def test_filter_my_tasks(self):
        data = {
            'my_task': 'on'
        }
        Task.objects.create(
            name='Task second',
            description='second description',
            status=self.status,
            executor=self.executor,
            author=self.executor
        )
        self.client.force_login(user=self.test_author)
        url = reverse_lazy('tasks_index')
        tasks = Task.objects.all()
        self.assertEquals(len(tasks), 2)
        response = self.client.get(url)
        response.user = self.test_author
        filter_queryset = TaskFilter(data, tasks, request=response).qs
        self.assertIn(self.first_task, filter_queryset)
        self.assertTrue(len(filter_queryset), 1)
