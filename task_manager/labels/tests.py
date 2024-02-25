from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.labels.models import Label
from django.core.exceptions import ObjectDoesNotExist
from django.test import tag
# Create your tests here.


@tag("app_name")
class LabelCrudTest(TestCase):

    def setUp(self):
        self.label_test = Label.objects.create(
            name='test label'
        )

    def test_create_label(self):
        data = {
            'name': 'worked',
        }
        url = reverse_lazy('marked:create label')
        response = self.client.post(url, data, format='json')
        self.assertRedirects(response, reverse_lazy('marked:labels_index'), status_code=302)
        label = Label.objects.get(name=data['name'])
        self.assertEqual(label.name, data['name'])

    def test_update_label(self):
        update_data = {
            'name': 'fix it'
        }
        url = reverse_lazy('marked:update label', args=[self.label_test.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data=update_data)
        self.label_test.refresh_from_db()
        self.assertEqual(self.label_test.name, update_data['name'])
        url_back = reverse_lazy('marked:labels_index')
        self.assertRedirects(response, url_back, status_code=302)

    def test_delete_label(self):
        before_count_status = len(Label.objects.all())
        self.assertEqual(before_count_status, 1)
        key = self.label_test.pk
        url = reverse_lazy('marked:delete label', kwargs={'pk': key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(url)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=key)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('marked:labels_index'))
