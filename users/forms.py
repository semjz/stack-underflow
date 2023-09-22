from django import forms

from .models import User


class UserUpdateForm(forms.ModelForm):
    pass


class UserRegisterForm(UserUpdateForm):
    pass


class UserLoginForm(forms.Form):
    pass