from django.shortcuts import render, HttpResponse
from posts.models import Post


def text_view(request):
    return HttpResponse("Текстовый ответ!")


def template_view(request):
    return render(request, "base.html")


def post_list_view(request):
    posts = Post.objects.all()
    return HttpResponse(posts)
