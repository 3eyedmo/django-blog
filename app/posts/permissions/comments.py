from rest_framework.permissions import BasePermission


class IsCommentPostOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.post.author == request.user:
            return True
        return False

class IsCommentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False

class IsCommentPostOwnerFollower(BasePermission):
    def has_object_permission(self, request, view, obj):
        post_owner = obj.post.author
        current_user = request.user
        if post_owner.has_follower(current_user):
            return True
        return False


