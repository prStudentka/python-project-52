from django.contrib import messages
from django.shortcuts import redirect
from .forms import *
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, get_user_model
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .mixin import UserLoginPassesMixin


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

	
class UserUpdateView(UserLoginPassesMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = get_user_model()  
    form_class = RegistrationForm
    context_object_name = 'form'
    #redirect_field_name = 'users_index'
    success_url = reverse_lazy('users_index')
    success_message = _("User successfully updated!")
    extra_context = {'title': _('Update user'), 'button': _('Update')}


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


class UserDeleteView(UserLoginPassesMixin, SuccessMessageMixin, DeleteView):
    template_name = 'form.html'
    model = CustomUser
    success_url = reverse_lazy('users_index')
    info_message = _('Are you sure you want to delete')
    success_message = _("User is successfully deleted!")
    extra_context = {'title': _('Delete user'), 'button': _('Yes, delete'), 'text': info_message}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = f'<p>{self.info_message} {self.request.user}?</p>'
        return context