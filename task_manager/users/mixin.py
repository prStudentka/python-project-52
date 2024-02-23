from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.shortcuts import redirect


class UserLoginPassesMixin(LoginRequiredMixin, UserPassesTestMixin):
    error_login_message = _('You are not logged in! Please log in.')
    error_permission_message = _('You do not have permissions to change this user')

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
