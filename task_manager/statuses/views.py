from django.shortcuts import render
#from .forms import *
from .models import *
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class IndexView(ListView):
    template_name = 'statuses.html'
    model = Status
    context_object_name = 'statuses'
    extra_context = {'title': _('Statuses'), 'button': _('Create status')}

	
class StatusCreateView(SuccessMessageMixin, CreateView):
    template_name = 'form_status.html'    
    model = Status
    context_object_name = 'form'
    fields = ['name']
    success_url = reverse_lazy('status_index')
    success_message = _("Status successfully created")
    extra_context = {'title': _('Create status'), 'button': _('Create')}


class StatusUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'form_status.html'    
    model = Status
    context_object_name = 'form'
    fields = ['name',]
    success_url = reverse_lazy('status_index')
    success_message = _("Status successfully updated")
    extra_context = {'title': _('Update status'), 'button': _('Update')}


class StatusDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'form_status.html'    
    model = Status
    context_object_name = 'form'
    success_url = reverse_lazy('status_index')
    info_message = _('Are you sure you want to delete')
    success_message = _("Status successfully deleted")
    extra_context = {'title': _('Delete status'), 'button': _('Yes, delete'), 'text': info_message, 'new_class': 'btn btn-danger'}
	
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = f'<p>{self.info_message} {self.object.name}?</p>'
        return context