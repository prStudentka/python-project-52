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
    template_name = 'tasks.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    extra_context = {'title': _('Tasks'), 'button': _('Create task'), 'button_filter': _('Show')}


class TaskCreateView(SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    model = Task
    context_object_name = 'form'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('tasks_index')
    success_message = _("Task successfully created")
    extra_context = {'title': _('Create task'), 'button': _('Create')}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = Task
    context_object_name = 'form'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('tasks_index')
    success_message = _("Task successfully updated")
    extra_context = {'title': _('Update task'), 'button': _('Update')}


class TaskDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'form.html'
    model = Task
    context_object_name = 'form'
    redirect_url = 'tasks_index'
    success_url = reverse_lazy(redirect_url)
    info_message = _('Are you sure you want to delete')
    success_message = _('Task successfully deleted')

    error_message = _('Only author of the task can delete it')
    extra_context = {'title': _('Delete task'),
                     'button': _('Yes, delete'),
                     'text': info_message,
                     'new_class': 'btn btn-danger'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = f'<p>{self.info_message} {self.object.name}?</p>'
        return context

    def post(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            messages.error(request, self.error_message)
            return redirect('tasks_index')
        return super().post(request, *args, **kwargs)


class TaskDetailView(SuccessMessageMixin, DetailView):
    template_name = 'task.html'
    model = Task
    context_object_name = 'task'
