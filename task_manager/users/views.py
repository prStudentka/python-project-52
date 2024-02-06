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
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
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

	
class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = get_user_model()  
    form_class = RegistrationForm
    context_object_name = 'form'
    #redirect_field_name = 'users_index'
    success_url = reverse_lazy('users_index')
    error_login_message = _('You are not logged in! Please log in.')
    error_permission_message = _('You do not have permissions to change this user')
    success_message = _("User successfully updated!")
    extra_context = {'title': _('Update user'), 'button': _('Update')}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.error_login_message)
            return redirect(reverse_lazy('users_index'))
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.warning(self.request, self.error_permission_message)
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


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin, DeleteView):
    template_name = 'form.html'
    model = CustomUser
    success_url = reverse_lazy('users_index')
    info_message = _('Are you sure you want to delete')
    success_message = _("User is successfully deleted!")
    error_login_message = _('You are not logged in! Please log in.')
    error_permission_message = _('You do not have permissions to change this user')
    extra_context = {'title': _('Delete user'), 'button': _('Yes, delete'), 'text': info_message}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.error_login_message)
            return redirect(reverse_lazy('users_index'))
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.warning(self.request, self.error_permission_message)
        return redirect(reverse_lazy('users_index'))
	
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = f'<p>{self.info_message} {self.request.user}?</p>'
        return context