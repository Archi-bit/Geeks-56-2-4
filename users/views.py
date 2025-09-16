from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate

def register_view(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "users/register.html", context={"form": form})
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "users/register.html", context={"form": form})
        elif form.is_valid():
            form.cleaned_data.__delitem__("password_confirm")
            user = User.objects.create_user(**form.cleaned_data)
            return redirect("/")
        
def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "users/login.html", context={"form": form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "users/login.html", context={"form": form})
        elif form.is_valid():
            user = authenticate(**form.cleaned_data)
            if not user:
                form.add_error(None, "User with given credential does not exist, try again!!!")
                return render(request, "users/login.html", context={"form": form})
            elif user:
                login(request, user)
                return redirect("/")
            
def logout_view(request):
    logout(request)
    return redirect("/")