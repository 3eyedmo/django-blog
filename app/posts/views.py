from django.contrib.auth import get_user_model


from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema


from .models import Post, Comment
from posts.serializers import (
    PostSerializer,
    CommentSerializer
)
from .permissions import (
    IsOwnerFollower,
    IsOwner,
    HasNotLiked,
    HasLiked,
    IsTargetUserFollower,
    IsCurrentUser
)
from posts.permissions import (
    IsCommentPostOwner,
    IsCommentOwner,
    IsCommentPostOwnerFollower
)


class PermissionPolicyMixin:
    def check_permissions(self, request):
        try:
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)




class LikeActionMixin:
    """
    This mixin is for liking a post.
    """

    @action(detail=True, methods=["post",])
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        post.likes.add(user)
        return Response(
            data= {
                "msg": "liked" 
            },
            status=status.HTTP_200_OK
        )



class UnlikeActionMixin:
    """
    This mixin is for unliking a post.
    """
    
    @action(detail=True, methods=["post",])
    def unlike(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        post.likes.remove(user)
        return Response(
            data= {
                "msg": "unliked" 
            },
            status=status.HTTP_200_OK
        )




class PostDetailActions(
    PermissionPolicyMixin,
    LikeActionMixin,
    UnlikeActionMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):

    """
    This api's aim to do CRUD operation for posts and some aditional 
    actions like , like and unlike.
    """
    parser_classes = (MultiPartParser,)
    permission_classes_per_method = {
        "retrieve": [IsAuthenticated , IsOwnerFollower | IsOwner],
        "destroy": [IsAuthenticated, IsOwner],
        "update": [IsAuthenticated, IsOwner],
        "partial_update": [IsAuthenticated, IsOwner],
        "like": (IsAuthenticated, IsOwnerFollower | IsOwner, HasNotLiked),
        "unlike": (IsAuthenticated, IsOwnerFollower | IsOwner, HasLiked)
    }
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_serializer_context(self, **kwargs):
        context = super().get_serializer_context(**kwargs)
        context["request"] = self.request
        return context

    def get_serializer_class(self):
        if self.action in ["like", "unlike"]:
            return None
        return super().get_serializer_class()




User = get_user_model()

class GetUserPosts(
    PermissionPolicyMixin,
    generics.ListAPIView
):
    serializer_class = PostSerializer
    permission_classes_per_method = {
        "get": [IsAuthenticated , IsTargetUserFollower | IsCurrentUser]
    }

    @swagger_auto_schema(
        operation_description="This api gives posts of a special user."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.get_object()
        qs = Post.objects.filter(author=user)
        return qs

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        try:
            obj = User.objects.get(id=user_id)
        except:
            raise NotFound
        self.check_object_permissions(self.request, obj=obj)
        return obj




class CreatePostView(
    PermissionPolicyMixin,
    generics.CreateAPIView
):
    """
    This api aims to create a post
    """
    parser_classes = (MultiPartParser,)
    serializer_class = PostSerializer
    permission_classes_per_method = {
        "post": [IsAuthenticated,]
    }



class FeedPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthenticated,
    )

    @swagger_auto_schema(
        operation_description="This api gives the feed posts. posts tha belongs to users followings."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        posts = Post.objects.filter(
            author__follow_req__from_user = self.request.user,
            author__follow_req__status = 'A'
            )
        return posts





        

class CommentRetrieveUpdateDestroy(
    PermissionPolicyMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    """
    This viewset represent CRUD operation for Comments.
    """
    permission_classes_per_method = {
        "retrieve": [IsAuthenticated, IsCommentOwner | IsCommentPostOwnerFollower | IsCommentPostOwner],
        "update": [IsAuthenticated, IsCommentOwner],
        "partial_update": [IsAuthenticated, IsCommentOwner],
        "destroy": [IsAuthenticated, IsCommentOwner | IsCommentPostOwner]
    }
    serializer_class = CommentSerializer


    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post__id = post_id)
        return queryset

    def get_object(self):
        obj = self.get_comment()
        self.check_object_permissions(request=self.request, obj=obj)
        return obj

    def get_comment(self):
        comment_id = self.kwargs.get("pk")
        try:
            obj = Comment.objects.select_related("post__author", "user").get(id = comment_id)
        except:
            raise NotFound()
        return obj

    def get_serializer_context(self, **kwargs):
        context = super().get_serializer_context(**kwargs)
        context["post"] = self.get_comment().post
        return context
    
    @swagger_auto_schema(request_body=CommentSerializer)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=CommentSerializer)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    


class CommentListCreate(
    PermissionPolicyMixin,
    generics.ListCreateAPIView
):

    """
    This api's operate as crud for comments.
    """
    permission_classes_per_method = {
        "post": [IsAuthenticated, IsOwnerFollower | IsOwner],
        "get": [IsAuthenticated, IsOwnerFollower | IsOwner]
    }
    serializer_class = CommentSerializer

    
    def get_queryset(self):
        post = self.get_post()
        queryset = post.comments.all()
        return queryset

    def get_post(self):
        post_id = self.kwargs.get("post_id")
        try:
            post = Post.objects.get(id = post_id)
        except:
            raise NotFound()
        self.check_object_permissions(request=self.request, obj=post)
        return post

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["post"] = self.get_post()
        return context
    
    @swagger_auto_schema(operation_description="This ep makes comments.", request_body=CommentSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    


