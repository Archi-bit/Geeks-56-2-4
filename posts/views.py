from django.shortcuts import render, HttpResponse
from posts.models import Post


def text_view(request):
    return HttpResponse("Текстовый ответ!")


def template_view(request):
    return render(request, "base.html")


def post_list_view(request):
    posts = Post.objects.all()
    return render(request, "posts/post_list.html", context={"posts_list": posts})

def post_detail_view(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, "post_detail.html", context={"post": post})