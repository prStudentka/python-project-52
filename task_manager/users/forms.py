from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegistrationForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):
        model = CustomUser

        fields = ('first_name', 'last_name', 'username','password1', 'password2')
        widgets = {
                'first_name': forms.TextInput(attrs={'required': True}),
				'last_name': forms.TextInput(attrs={'required': True}),
        }