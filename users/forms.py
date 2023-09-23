from django import forms
from .models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "national_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already exist!")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already exist!")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserRegisterForm(UserUpdateForm):
    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "national_id", "password"]

    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if not (confirm_password and password):
            raise forms.ValidationError("Enter the both of password")
        if confirm_password != password:
            raise forms.ValidationError("Password must match ")
        return confirm_password


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=15, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
