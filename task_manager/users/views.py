from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, get_user_model
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy



class IndexView(ListView):
    template_name = 'users.html'
    model = CustomUser
    context_object_name = 'users'
    extra_context = {'title': _('Users')}
    #paginate_by = 10


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'form.html'    
    form_class = RegistrationForm
    context_object_name = 'form'
    success_url = reverse_lazy('log in')
    success_message = _("User is successfully registered")
    extra_context = {'title': _('Registration'), 'button': _('Register')}

	
class UserUpdateView(  UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = get_user_model()  
    form_class = RegistrationForm
    context_object_name = 'form'
    success_url = reverse_lazy('users_index')
    success_message = _("User successfully updated!")
    error_message = _('You do not have permissions to change this user')
    extra_context = {'title': _('Update user'), 'button': _('Update')}

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.warning(self.request, _('You do not have permissions to change this user'))
        return redirect(reverse_lazy('users_index'))


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('index')
    context_object_name = 'form'
    success_message = _("You are logged in")
    extra_context = {'title': _('Entrance'), 'button': _('Enter')}


def user_logout(request):
    logout(request)
    messages.info(request, _("You are logged out"))
    return redirect('index')


class UserDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'form.html'
    model = CustomUser
    success_url = reverse_lazy('users_index')
    success_message = _("User successfully deleted!")
    extra_context = {'title': _('Delete user'), 'button': _('Yes, delete'), 'delete': 'delete'}