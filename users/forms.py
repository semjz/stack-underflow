from django import forms
from .models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "national_id"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already exist!")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(emai=email).exists():
            raise forms.ValidationError("This email is already exist!")


class UserRegisterForm(UserUpdateForm):
    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "national_id", "password"]

    confirm_password = forms.CharField(max_length=128)

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if confirm_password != password:
            raise forms.ValidationError("Password must match ")
        if not confirm_password or not password:
            raise forms.ValidationError("Enter the both of password")


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=15, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
