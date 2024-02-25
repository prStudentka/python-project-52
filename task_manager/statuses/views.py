from .models import Status
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixin import DeleteProtectedMixin


# Create your views here.
class IndexView(ListView):
    template_name = 'statuses.html'
    model = Status
    context_object_name = 'statuses'
    extra_context = {'title': _('Statuses'), 'button': _('Create status')}


class StatusCreateView(SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    model = Status
    context_object_name = 'form'
    fields = ['name']
    success_url = reverse_lazy('status_index')
    success_message = _("Status successfully created")
    extra_context = {'title': _('Create status'), 'button': _('Create')}


class StatusUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = Status
    context_object_name = 'form'
    fields = ['name', ]
    success_url = reverse_lazy('status_index')
    success_message = _("Status successfully updated")
    extra_context = {'title': _('Update status'), 'button': _('Update')}


class StatusDeleteView(SuccessMessageMixin, DeleteProtectedMixin, DeleteView):
    template_name = 'form.html'
    model = Status
    context_object_name = 'form'
    redirect_url = 'status_index'
    success_url = reverse_lazy(redirect_url)
    info_message = _('Are you sure you want to delete')
    success_message = _("Status successfully deleted")
    error_message = _('You can\'t to delete because status was used')
    extra_context = {'title': _('Delete status'), 'button': _('Yes, delete'), 'text': info_message,
                     'new_class': 'btn btn-danger'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = f'<p>{self.info_message} {self.object.name}?</p>'
        return context
