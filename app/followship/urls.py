from django.urls import path
from .views import (
    FollowRequestView,
    RequestCancel,
    RequestIgnore,
    RemoveFollower,
    Unfollow,
    RequestAccept,
    GetFollowersView,
    GetFollowingView
)

app_name = 'followship'
urlpatterns= [
    path("follow_request/<int:pk>/", FollowRequestView.as_view(), name="follow_request"),
    path("request_cancel/<int:pk>/", RequestCancel.as_view(), name="request_cancel"),
    path("unfollow/<int:pk>/", Unfollow.as_view(), name="unfollow"),
    path("request_accept/<int:pk>/", RequestAccept.as_view(), name="request_accept"),
    path("request_ignore/<int:pk>/", RequestIgnore.as_view(), name="request_ignore"),
    path("remove_follower/<int:pk>/", RemoveFollower.as_view(), name="remove_follower"),
    path("followers/<int:pk>/", GetFollowersView.as_view(), name="get_followers"),
    path("followings/<int:pk>/", GetFollowingView.as_view(), name="get_followings")
]