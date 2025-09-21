from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from posts.models import Post, Category
from users.models import Profile
from django.views.generic import TemplateView
from django.db.models import Q



class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search", "")
        category_id = self.request.GET.get("category", "")
        order = self.request.GET.get("order", "")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if order == "rate":
            queryset = queryset.order_by("-rate")
        elif order == "created":
            queryset = queryset.order_by("-created_at")
        elif order == "title":
            queryset = queryset.order_by("title")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["search"] = self.request.GET.get("search", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["order"] = self.request.GET.get("order", "")
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/post_form.html"
    fields = ["title", "content", "image"]
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "posts/post_form.html"
    fields = ["title", "content", "image", "rate", "category", "tags"]
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


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

class HomeView(TemplateView):
    template_name = "base.html"