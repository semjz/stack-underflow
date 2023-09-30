from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from users.models import User


# Create your views here.
def user_register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "you registered successfully")
            login(request, user)
            return redirect("users:home")
        else:
            messages.warning(request, "register unsuccessfully")
    else:
        form = UserRegisterForm()

    return render(request, "user/user_register_form.html", {"form": form})


def user_login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "login successful")
                return redirect("users:home")
            else:
                messages.warning(request, "login unsuccessfully")
    else:
        form = UserLoginForm()

    return render(request, "user/user_login_form.html", {"form": form})


def user_logout_view(request):
    logout(request)
    return redirect("users:home")


def user_profile_view(request, uid):
    user = User.objects.get(id=uid)
    return render(request, "user/user_profile_view.html", {"user": user})


def user_profile_edit_view(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserUpdateForm()
    return render(request, "user/user_edit.html", {"form": form})


def user_home_view(request):
    return render(request, 'home.html')
