from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema

from .serializers import ProfileSerializer
from .models import Profile
from .permissions import IsProfileOwner
from posts.views import PermissionPolicyMixin



class RetrieveUpdateProfile(PermissionPolicyMixin,
                            UpdateModelMixin,
                            RetrieveModelMixin,
                            GenericViewSet):
    """
    This View is for updating, retrieving and deleting of an special user profile.
    """

    model = Profile
    serializer_class = ProfileSerializer
    permission_classes_per_method = {
        "retrieve": (IsAuthenticated, ),
        "update": (IsAuthenticated, IsProfileOwner),
        "destroy": (IsAuthenticated, IsProfileOwner),
        "partial_update": (IsAuthenticated, IsProfileOwner)
    }
    parser_classes = (MultiPartParser, )

    def get_object(self):
        user_id = self.kwargs.get("pk")
        try:
            obj = Profile.objects.get(user__id = user_id)
        except:
            raise NotFound()
        self.check_object_permissions(self.request, obj)
        return obj

    @swagger_auto_schema(request_body=ProfileSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    
