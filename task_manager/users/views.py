from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login, get_user_model, update_session_auth_hash
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


class IndexView(ListView):
    template_name = 'users.html'
    model = CustomUser
    context_object_name = 'users'
    extra_context = {'title': _('Users')}
    #paginate_by = 10
    ''' def get(self, request, *args, **kwargs):
        list_users = CustomUser.objects.all()
        return render(request, 'users.html', context={'users': list_users})'''


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'form.html'    
    form_class = RegistrationForm
    context_object_name = 'form'
    success_url = reverse_lazy('log in')
    success_message = _("User is successfully registered")
    extra_context = {'title': _('Registration'), 'button': _('Register')}

	
class UserUpdateView( SuccessMessageMixin, UpdateView): #UserPassesTestMixin,
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
    '''
    
    def handle_no_permission(self):
        messages.warning(self.request, _('You do not have permissions to change this user'))
        return redirect('users_index')
	

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, _("You are loging"))
            return redirect('index')
        return redirect('log in')
    else:
        form = LoginForm()
        
    return render(request, 'login.html', context={'form': form})'''

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('index')
    context_object_name = 'form'
    success_message = _("You are logged in")
    extra_context = {'title': _('Entrance'), 'button': _('Enter')}
    '''
    def form_invalid(self, form):
        messages.error(self.request, _(
            'Пожалуйста, введите правильные имя пользователя и пароль. '
            'Оба поля могут быть чувствительны к регистру.'
        ))
        return super().form_invalid(form)
    '''

def user_logout(request):
    logout(request)
    messages.info(request, _("You are logged out"))
    return redirect('index')


'''
def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.info(request, _("User successfully registred!"))
            return redirect('log in')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})
'''

class UserDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'form.html'
    model = CustomUser
    success_url = reverse_lazy('users_index')
    success_message = _("User successfully deleted!")
    extra_context = {'title': _('Delete user'), 'button': _('Yes, delete'), 'delete': 'delete'}