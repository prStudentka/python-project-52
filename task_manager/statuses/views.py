from .models import Status
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixin import DeleteProtectedMixin


# Create your views here.
class IndexView(ListView):
    template_name = 'statuses/index.html'
    model = Status
    context_object_name = 'statuses'
    extra_context = {'title': _('Statuses'), 'button': _('Create status')}


class StatusCreateView(SuccessMessageMixin, CreateView):
    template_name = 'statuses/create.html'
    model = Status
    context_object_name = 'form'
    fields = ['name']
    success_url = reverse_lazy('status_index')
    success_message = _("Status successfully created")


class StatusUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'statuses/update.html'
    model = Status
    context_object_name = 'form'
    fields = ['name', ]
    success_url = reverse_lazy('status_index')
    success_message = _("Status successfully updated")


class StatusDeleteView(SuccessMessageMixin, DeleteProtectedMixin, DeleteView):
    template_name = 'statuses/delete.html'
    model = Status
    context_object_name = 'form'
    redirect_url = 'status_index'
    success_url = reverse_lazy(redirect_url)
    success_message = _("Status successfully deleted")
    error_message = _('You can\'t to delete because status was used')
