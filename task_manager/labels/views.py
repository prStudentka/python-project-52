from django.shortcuts import render
from .models import *
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixin import DeleteProtectedMixin


# Create your views here.
class LabelsView(ListView):
    template_name = 'labels.html'
    model = Label
    context_object_name = 'labels'
    extra_context = {'title': _('Labels'), 'button': _('Create label')}


class LabelCreateView(SuccessMessageMixin, CreateView):
    template_name = 'form.html'    
    model = Label
    context_object_name = 'form'
    fields = ['name']
    success_url = reverse_lazy('marked:labels_index')
    success_message = _("Label successfully created")
    extra_context = {'title': _('Create label'), 'button': _('Create')}


class LabelUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'form.html'    
    model = Label
    context_object_name = 'form'
    fields = ['name',]
    success_url = reverse_lazy('marked:labels_index')
    success_message = _("Label successfully updated")
    extra_context = {'title': _('Update label'), 'button': _('Update')}


class LabelDeleteView(SuccessMessageMixin, DeleteProtectedMixin, DeleteView):
    template_name = 'form.html'    
    model = Label
    context_object_name = 'form'
    redirect_url = 'marked:labels_index'
    success_url = reverse_lazy(redirect_url)
    info_message = _('Are you sure you want to delete')
    success_message = _("Label successfully deleted")
    error_message = _('You can\'t to delete because label was used')
    extra_context = {'title': _('Delete label'), 'button': _('Yes, delete'), 'text': info_message, 'new_class': 'btn btn-danger'}
	
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = f'<p>{self.info_message} {self.object.name}?</p>'
        return context