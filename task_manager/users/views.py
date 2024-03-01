from django.contrib import messages
from django.shortcuts import redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, get_user_model
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from task_manager.users.mixin import UserLoginPassesMixin
from task_manager.mixin import DeleteProtectedMixin


class IndexView(ListView):
    template_name = 'users/index.html'
    model = CustomUser
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    form_class = RegistrationForm
    context_object_name = 'form'
    success_url = reverse_lazy('log in')
    success_message = _("User is successfully registered")


class UserUpdateView(UserLoginPassesMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/update.html'
    model = get_user_model()
    form_class = RegistrationForm
    context_object_name = 'form'
    success_url = reverse_lazy('users_index')
    success_message = _("User successfully updated!")


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('index')
    context_object_name = 'form'
    success_message = _("You are logged in")


def user_logout(request):
    logout(request)
    messages.info(request, _("You are logged out"))
    return redirect('index')


class UserDeleteView(UserLoginPassesMixin, DeleteProtectedMixin, SuccessMessageMixin, DeleteView):
    template_name = 'users/delete.html'
    model = CustomUser
    redirect_url = 'users_index'
    success_url = reverse_lazy(redirect_url)
    success_message = _("User is successfully deleted!")
    error_message = _('You can\'t to delete user because he was used')
