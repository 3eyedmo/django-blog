from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission
from posts.models import LikeAction
from django.contrib.auth import get_user_model

User = get_user_model()
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.author == user:
            return True
        return False

class IsOwnerFollower(BasePermission):
    def has_object_permission(self, request, view, obj):
        target_user = obj.author
        current_user = request.user
        is_follower = current_user.has_following(target_user)
        if is_follower:
            return True
        return False


class IsTargetUserFollower(BasePermission):
    def has_object_permission(self, request, view, obj):
        super().has_object_permission(request, view, obj)
        current_user = request.user
        target_user = obj
        is_follower = current_user.has_following(target_user)
        if is_follower:
            return True
        return False




class CanVisitProfile(BasePermission):
    def has_permission(self, request, view):
        target_user_id = view.kwargs.get('id', '')
        current_user = request.user
        try:
            target_user = User.objects.get(id=target_user_id)
        except:
            raise NotFound
        is_follower = current_user.has_following(target_user)
        if is_follower:
            return True
        is_owner = current_user.id == target_user_id
        if is_owner:
            return True
        return False


class HasLiked(BasePermission):
    def has_object_permission(self, request, view, obj):
        if LikeAction.objects.filter(post=obj, user=request.user).exists():
            return True
        return False


class HasNotLiked(BasePermission):
    def has_object_permission(self, request, view, obj):
        if LikeAction.objects.filter(post=obj, user=request.user).exists():
            return False
        return True

class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        super().has_object_permission(request, view, obj)
        if obj == request.user:
            return True
        return False