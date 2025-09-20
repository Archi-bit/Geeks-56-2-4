from django.shortcuts import render, HttpResponse, redirect 
from posts.models import Post
from django.http import JsonResponse
from posts.forms import PostForm, PostModelForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q





def text_view(request):
    return HttpResponse("Текстовый ответ!")


def template_view(request):
    if request.method == "GET":
        return render(request, "base.html")

@login_required(login_url="/login/")
def post_list_view(request):
    posts = Post.objects.all()
    limit = 3
    if request.method == "GET":
        search = request.GET.get("search")
        category_id = request.GET.get("category_id")
        ordering = request.GET.get("ordering")
        page = int(request.GET.get("page", 1))
        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
        if category_id:
            posts = posts.filter(category_id=category_id)
        if ordering:
            posts = posts.order_by(ordering)
        if page:
            max_pages = posts.count() / limit
            if round(max_pages) < max_pages:
                max_pages = round(max_pages) + 1
            elif round(max_pages) > max_pages:
                max_pages = round(max_pages)
            start = (page - 1) * limit 
            end = page * limit
            posts = posts[start:end]
        form = SearchForm()
        return render(
            request, 
            "posts/post_list.html", 
            context={"posts_list": posts, "form": form, "max_pages": range(1, max_pages + 1)},
        )

@login_required(login_url="/login/")
def post_detail_view(request, post_id):
    if request.method == "GET":
        post = Post.objects.get(id=post_id)
        return render (request, "posts/post_detail.html", context={'post': post})

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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
        
@login_required(login_url="/login/")
def post_create_modelform_view(request):
    if request.method == "POST":
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("post_list")
    else:
        form = PostModelForm()
    
    return render(request, "posts/post_create_modelform.html", {"form": form})