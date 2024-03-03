from .models import Label
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixin import DeleteProtectedMixin


# Create your views here.
class LabelsView(ListView):
    template_name = 'labels/index.html'
    model = Label
    context_object_name = 'labels'


class LabelCreateView(SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/create.html'
    context_object_name = 'form'
    fields = ['name']
    success_url = reverse_lazy('marked:labels_index')
    success_message = _("Label successfully created")


class LabelUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'labels/update.html'
    model = Label
    context_object_name = 'form'
    fields = ['name',]
    success_url = reverse_lazy('marked:labels_index')
    success_message = _("Label successfully updated")


class LabelDeleteView(SuccessMessageMixin, DeleteProtectedMixin, DeleteView):
    redirect_url = 'marked:labels_index'
    template_name = 'labels/delete.html'
    model = Label
    context_object_name = 'form'
    success_url = reverse_lazy(redirect_url)
    success_message = _("Label successfully deleted")
    error_message = _('You can\'t to delete because label was used')
