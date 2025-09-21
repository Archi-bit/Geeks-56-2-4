from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from users.models import Profile
from posts.models import Post
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

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
            age = form.cleaned_data.pop("age")
            avatar = form.cleaned_data.pop("avatar")
            user = User.objects.create_user(**form.cleaned_data)
            if user:
                Profile.objects.create(user=user, age=age, avatar=avatar)
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
            
@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("/")

class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(author=self.request.user)
        return context