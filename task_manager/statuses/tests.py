from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.statuses.models import Status
from django.core.exceptions import ObjectDoesNotExist


# Create your tests here.
class StatusCrudTest(TestCase):

    def setUp(self):
	    self.status_test = Status.objects.create(
		    name='test status'
		)
	    data = {
	       'name': 'worked',
        }


    def test_create_status(self):
	    data = {
	       'name': 'worked',
        }
	    url = reverse_lazy('create status')		
	    response = self.client.post(url, data, format='json')
	    self.assertRedirects(response, reverse_lazy('status_index'), status_code=302)
	    status = Status.objects.get(name=data['name'])
	    self.assertEqual(status.name, data['name'])

	
    def test_update_status(self):
        update_data = {
	       'name': 'fix it'
        }
        url = reverse_lazy('update status', args=[self.status_test.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data=update_data)
        self.status_test.refresh_from_db()
        self.assertEqual(self.status_test.name, update_data['name'])
        self.assertRedirects(response, reverse_lazy('status_index'), status_code=302)

	
    def test_delete_status(self):
        before_count_status = len(Status.objects.all())
        self.assertEqual(before_count_status, 1)
        key = self.status_test.pk
        url = reverse_lazy('delete status', kwargs={'pk': key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(url)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=key)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('status_index'))