from django.contrib import admin
from .models import Post, Comment, LikeAction


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "author",
        "created",
        "updated"
    ]

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "post",
        "user"
    ]

admin.site.register(Comment, CommentAdmin)

class LikeActionAdmin(admin.ModelAdmin):
    list_display = [
        "post",
        "user",
        "created"
    ]

admin.site.register(LikeAction, LikeActionAdmin)