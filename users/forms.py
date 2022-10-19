from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email']
        # valid_email = False
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        else:
            try:
                validate_email(email)

            except ValidationError as e:
                raise ValidationError("Bad Email")
