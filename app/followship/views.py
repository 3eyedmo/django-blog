from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import FollowRequests
from .permissions import (
    HasNotFollowedOrRequested,
    HasRequested,
    HasBeenRequested,
    IsFollower,
    IsFollowing,
    IsProfileOwner
)
from .serializers import PeopleSerializer


User = get_user_model()


class GetObjectMixin:

    def get_object(self):
        try:
            pk = self.kwargs.get("pk")
            obj = self.model.objects.get(id = pk)
        except:
            raise NotFound
        self.check_object_permissions(request=self.request, obj=obj)
        return obj

class FollowRequestView(
    GetObjectMixin,
    generics.GenericAPIView
):

    permission_classes = (
        IsAuthenticated,
        HasNotFollowedOrRequested
    )
    model = User

    @swagger_auto_schema(
        operation_description="This api send follow request to a target user"
    )
    def post(self, request, *args, **kwargs):
        self.perform_follow_request()
        return Response(status=status.HTTP_200_OK)

    def perform_follow_request(self):
        from_user = self.request.user
        to_user = self.get_object()
        from_user.followings.add(to_user)



class RequestCancel(
    GetObjectMixin,
    generics.GenericAPIView
):

    permission_classes = (
        IsAuthenticated,
        HasRequested
    )
    model = User

    @swagger_auto_schema(
        operation_description="This api cancel a follow request to a target user"
    )
    def post(self, request, *args, **kwargs):
        self.perform_request_cancel()
        return Response(status=status.HTTP_200_OK)


    def perform_request_cancel(self):
        from_user = self.request.user
        to_user = self.get_object()
        from_user.followings.remove(to_user)


class RequestAccept(
    GetObjectMixin,
    generics.GenericAPIView
):
    permission_classes = (
        IsAuthenticated,
        HasBeenRequested
    )
    model = User

    @swagger_auto_schema(
        operation_description="In this api user accept a follow request"
    )
    def post(self, request, *args, **kwargs):
        self.perform_accept()
        return Response(status=status.HTTP_200_OK)


    def perform_accept(self):
        to_user = self.request.user
        from_user = self.get_object()
        follow_req = FollowRequests.objects.get(
            from_user=from_user,
            to_user=to_user
        )
        follow_req.status = FollowRequests.FollowshipStatus.ACCEPTED
        follow_req.save()



class RequestIgnore(
    GetObjectMixin,
    generics.GenericAPIView
):
    permission_classes = (
        IsAuthenticated,
        HasBeenRequested
    )
    model = User

    @swagger_auto_schema(
        operation_description="In this api user ignore a follow request"
    )
    def post(self, request, *args, **kwargs):
        self.perform_ignore()
        return Response(status=status.HTTP_200_OK)


    def perform_ignore(self):
        to_user = self.request.user
        from_user = self.get_object()
        follow_req = FollowRequests.objects.get(
            from_user=from_user,
            to_user=to_user
        )
        follow_req.delete()


class Unfollow(
    GetObjectMixin,
    generics.GenericAPIView
):
    permission_classes = (
        IsAuthenticated,
        IsFollower
    )
    model = User
    serializer_class = None

    @swagger_auto_schema(
        operation_description="In this api user unfollow a another user"
    )
    def post(self, request, *args, **kwargs):
        self.perform_unfollow()
        return Response(status=status.HTTP_200_OK)


    def perform_unfollow(self):
        to_user = self.request.user
        from_user = self.get_object()
        to_user.followings.remove(from_user)


class RemoveFollower(
    GetObjectMixin,
    generics.GenericAPIView
):
    permission_classes = (
        IsAuthenticated,
        IsFollowing
    )
    model = User

    @swagger_auto_schema(
        operation_description="In this user remove one of follower"
    )
    def post(self, request, *args, **kwargs):
        self.perform_remove_follower()
        return Response(status=status.HTTP_200_OK)


    def perform_remove_follower(self):
        to_user = self.request.user
        from_user = self.get_object()
        follow_req = FollowRequests.objects.get(
            from_user=from_user,
            to_user=to_user
        )
        follow_req.delete()




class GetFollowersView(
    GetObjectMixin,
    generics.ListAPIView
):
    permission_classes = (
        IsAuthenticated,
        IsProfileOwner | IsFollower
    )
    serializer_class = PeopleSerializer
    model = User

    @swagger_auto_schema(
        operation_description="this api get list of followings"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        target_user = self.get_object()
        qs = target_user.get_followers()
        serializer = self.serializer_class(qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetFollowingView(
    GetObjectMixin,
    generics.ListAPIView
):
    permission_classes = (
        IsAuthenticated,
        IsProfileOwner | IsFollower
    )
    serializer_class = PeopleSerializer
    model = User

    @swagger_auto_schema(
        operation_description="this api get list of followings"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        target_user = self.get_object()
        qs = target_user.get_followings()
        return qs