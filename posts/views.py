from django.shortcuts import render, HttpResponse
from posts.models import Post
from django.http import JsonResponse


def text_view(request):
    return HttpResponse("Текстовый ответ!")


def template_view(request):
    return render(request, "base.html")


def post_list_view(request):
    posts = Post.objects.all()
    return render(request, "posts/post_list.html", context={"posts_list": posts})

def post_detail_view(request, post_id):
    post = Post.objects.get(id=post_id)
    return render (request, "posts/post_detail.html", context={'post': post})


def post_detail_api(request, post_id):
    from .models import Post
    post = Post.objects.get(id=post_id)
    data = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "rate": post.rate,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "category": post.category.name if post.category else None,
        "tags": [tag.name for tag in post.tags.all()],
        "image": post.image.url if post.image else None,
    }
    return JsonResponse(data)