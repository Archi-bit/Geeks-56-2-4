from django.contrib import admin
from posts.models import Post, Category, Tag


admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "rate", "created_at", "category", )
    list_display_links = ("title", "content",)