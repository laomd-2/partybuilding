# users/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}), max_length=8)
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        min_length=6, max_length=20
    )
