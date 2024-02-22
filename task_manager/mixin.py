from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError


class DeleteProtectedMixin:
    error_message = None
    redirect_url = None
	
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.error_message)
            return redirect(self.redirect_url)