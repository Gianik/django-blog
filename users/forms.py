from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", 'first_name', 'last_name', "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar']


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
