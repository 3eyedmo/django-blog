from rest_framework.permissions import BasePermission
from .models import FollowRequests as FR

class HasNotFollowedOrRequested(BasePermission):
    def has_object_permission(self, request, view, obj):
        from_user = request.user
        if FR.objects.filter(from_user=from_user, to_user=obj).exists():
            return False
        return True

class HasRequested(BasePermission):
    def has_object_permission(self, request, view, obj):
        from_user = request.user
        to_user = obj
        if FR.objects.filter(from_user=from_user, to_user=to_user, status="P").exists():
            return True
        return False

class HasBeenRequested(BasePermission):
    def has_object_permission(self, request, view, obj):
        to_user = request.user
        from_user = obj
        if FR.objects.filter(from_user=from_user, to_user=to_user, status="P").exists():
            return True
        return False


class IsFollower(BasePermission):
    def has_object_permission(self, request, view, obj):
        from_user = request.user
        to_user = obj
        if FR.objects.filter(from_user=from_user, to_user=to_user, status=FR.FollowshipStatus.ACCEPTED).exists():
            return True
        return False

class IsFollowing(BasePermission):
    def has_object_permission(self, request, view, obj):
        to_user = request.user
        from_user = obj
        if FR.objects.filter(from_user=from_user, to_user=to_user, status=FR.FollowshipStatus.ACCEPTED).exists():
            return True
        return False

class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        target_user = obj
        current_user = request.user
        if target_user == current_user:
            return True
        return False