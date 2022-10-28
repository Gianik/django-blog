
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", 'first_name', 'last_name', "password1", "password2")

    def clean_email(self,  *args, **kwargs):
        email = self.cleaned_data.get("email")

        if not "@" in email or not email.endswith(".com"):
            raise forms.ValidationError("This is not a valid email")
        return email

    def clean_first_name(self,  *args, **kwargs):
        first_name = self.cleaned_data.get("first_name")

        if not first_name:
            raise forms.ValidationError("Empty Or Invalid First Name")

        if not first_name.isalpha():
            raise forms.ValidationError(
                "Numbers and Special Characters in First Name is not allowed")

        if len(first_name) > 80:
            raise forms.ValidationError("First Name Input exceeds max length")
        return first_name

    def clean_last_name(self,  *args, **kwargs):
        last_name = self.cleaned_data.get("last_name")

        if not last_name:
            raise forms.ValidationError("Empty Or Invalid Last Name")

        if not last_name.isalpha():
            raise forms.ValidationError(
                "Numbers and Special Characters in Last Name is not allowed")

        if len(last_name) > 80:
            raise forms.ValidationError("Last Name Input exceeds max length")
        return last_name


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']

    def clean_first_name(self,  *args, **kwargs):
        first_name = self.cleaned_data.get("first_name")

        if not first_name:
            raise forms.ValidationError("Empty Or Invalid First Name")

        if not first_name.isalpha():
            raise forms.ValidationError(
                "Numbers and Special Characters in First Name is not allowed")

        if len(first_name) > 80:
            raise forms.ValidationError("First Name Input exceeds max length")
        return first_name

    def clean_last_name(self,  *args, **kwargs):
        last_name = self.cleaned_data.get("last_name")

        if not last_name:
            raise forms.ValidationError("Empty Or Invalid Last Name")

        if not last_name.isalpha():
            raise forms.ValidationError(
                "Numbers and Special Characters in Last Name is not allowed")

        if len(last_name) > 80:
            raise forms.ValidationError("Last Name Input exceeds max length")
        return last_name


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=500)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self,  *args, **kwargs):
        email = self.cleaned_data.get("email")

        if not "@" in email or not email.endswith(".com"):
            raise forms.ValidationError("This is not a valid email")
        return email
