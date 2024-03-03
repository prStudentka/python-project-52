from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from task_manager.tasks.filters import TaskFilter
from django.core.management import call_command


# Create your tests here.
class TaskCrudTest(TestCase):

    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        call_command('loaddata', 'users.json', verbosity=2)
        call_command('loaddata', 'statuses.json', verbosity=2)
        call_command('loaddata', 'tasks.json', verbosity=2)
        self.test_author = CustomUser.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)
        self.executor = CustomUser.objects.create_user(
            first_name='Pizza',
            last_name='Delivery',
            username='user_test',
            password='i12345'
        )
        self.label1 = Label.objects.create(name='label test one')
        self.first_task = Task.objects.get(pk=1)
        self.first_task.labels.add(self.label1)
        self.data = {
            'name': 'Task was created for test',
            'description': 'test description',
            'status': self.status.pk,
            'executor': self.executor.pk,
            'author': self.test_author.pk
        }

    def test_create_task(self):
        url = reverse_lazy('create task')
        self.client.force_login(user=self.test_author)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, self.data, format='json', follow=True)
        url_back = reverse_lazy('tasks_index')
        self.assertRedirects(response, url_back, status_code=302)
        task_name = Task.objects.get(name=self.data['name'])
        self.assertEqual(task_name.name, self.data['name'])

    def test_update_task(self):
        old_name_task = self.first_task.name
        self.client.force_login(user=self.test_author)
        url = reverse_lazy('update task', args=[self.first_task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data=self.data)
        self.first_task.refresh_from_db()
        self.assertEqual(self.first_task.name, self.data['name'])
        self.assertEqual(self.first_task.name != old_name_task, True)
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
        self.assertTemplateUsed(response, template_name='tasks/task.html')

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
