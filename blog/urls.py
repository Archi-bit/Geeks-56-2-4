from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from posts.views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, HomeView
)
from users.views import register_view, login_view, logout_view, ProfileView

users_patterns = [
    path("register/", register_view), 
    path("login/", login_view), 
    path("logout/", logout_view), 
    path("profile/", ProfileView.as_view(), name="profile"),
]

urlpatterns = users_patterns + [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('posts/', PostListView.as_view(), name="post_list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('posts/create/', PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
