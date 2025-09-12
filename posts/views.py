from django.shortcuts import render, HttpResponse, redirect 
from posts.models import Post
from django.http import JsonResponse
from posts.forms import PostForm, PostModelForm


def text_view(request):
    return HttpResponse("Текстовый ответ!")


def template_view(request):
    if request.method == "GET":
        return render(request, "base.html")


def post_list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        return render(request, "posts/post_list.html", context={"posts_list": posts})


def post_detail_view(request, post_id):
    if request.method == "GET":
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

def post_create_view(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "posts/post_create.html", context={"form": form})
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "posts/post_create.html", context={"form": form})
        elif form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            image = form.cleaned_data.get("image")
            post = Post.objects.create(title=title, content=content, image=image)
            return redirect ("/")
        

def post_create_modelform_view(request):
    if request.method == "POST":
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("post_list")
    else:
        form = PostModelForm()
    
    return render(request, "posts/post_create_modelform.html", {"form": form})