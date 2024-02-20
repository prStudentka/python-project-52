import django_filters
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser
from task_manager.tasks.models import Task
from django.utils.translation import gettext as _
from django.forms import CheckboxInput


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(field_name='status', queryset=Status.objects.all())
    labels = django_filters.ModelChoiceFilter(field_name='labels', queryset=Label.objects.all())
    my_task = django_filters.BooleanFilter(field_name='my_tasks', widget =CheckboxInput, label = _('Only my tasks'), method='filter_tasks' )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_tasks(self, queryset, name, value):
	    if not value:
		    return queryset
	    return queryset.filter(author=self.request.user)