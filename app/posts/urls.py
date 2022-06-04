from django.urls import path, include
from .views import (
    FeedPostsView,
    CreatePostView,
    GetUserPosts,
    PostDetailActions,
    CommentListCreate,
    CommentRetrieveUpdateDestroy
)
from rest_framework import routers

post_router = routers.DefaultRouter()
post_router.register(basename=r"post", viewset=PostDetailActions, prefix="post")

app_name = 'posts'
urlpatterns=[
    path("post/", CreatePostView.as_view(), name="create_post"),
    path("posts/<int:user_id>/", GetUserPosts.as_view(), name="get_posts"),
    path('posts/feed/', FeedPostsView.as_view(), name="feed"),
    path("", include(post_router.urls)),
    path("post/<int:post_id>/comment/", CommentListCreate.as_view(), name="comment_create_list"),
    path("post/<int:post_id>/comment/<int:pk>/", CommentRetrieveUpdateDestroy.as_view(), name="comment_delete_retreive_update"),
]