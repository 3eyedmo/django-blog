from rest_framework.permissions import BasePermission

class IsProfileUserFollower(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        target_user = obj.user
        if target_user.has_follower(current_user):
            return True
        return False

class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        target_user = obj.user
        if current_user == target_user:
            return True
        return False
