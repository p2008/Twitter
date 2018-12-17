from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label='email', max_length=64, required=True)
    password = forms.CharField(label='Hasło', max_length=64,
                               widget=forms.PasswordInput, required=True)


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)


class CreateUserForm(forms.Form):
    email = forms.EmailField(label='email', max_length=64, required=True)
    password1 = forms.CharField(max_length=32, required=True,
                                validators=[password_validation.validate_password],
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(max_length=32, required=True)
    first_name = forms.CharField(max_length=32, required=False)
    last_name = forms.CharField(max_length=32, required=False)


