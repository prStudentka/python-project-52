from django.shortcuts import redirect
from django.contrib import messages
from .models import Task
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from task_manager.tasks.filters import TaskFilter


# Create your views here.
class IndexView(FilterView):
    template_name = 'tasks/index.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    extra_context = {'button_filter': _('Show')}


class TaskCreateView(SuccessMessageMixin, CreateView):
    template_name = 'tasks/create.html'
    model = Task
    context_object_name = 'form'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('tasks_index')
    success_message = _("Task successfully created")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'tasks/update.html'
    model = Task
    context_object_name = 'form'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('tasks_index')
    success_message = _("Task successfully updated")


class TaskDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'tasks/delete.html'
    model = Task
    context_object_name = 'form'
    redirect_url = 'tasks_index'
    success_url = reverse_lazy(redirect_url)
    success_message = _('Task successfully deleted')
    error_message = _('Only author of the task can delete it')

    def post(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            messages.error(request, self.error_message)
            return redirect('tasks_index')
        return super().post(request, *args, **kwargs)


class TaskDetailView(SuccessMessageMixin, DetailView):
    template_name = 'tasks/task.html'
    model = Task
    context_object_name = 'task'
