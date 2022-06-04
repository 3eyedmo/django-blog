from django.urls import path, include
from .views import RetrieveUpdateProfile
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"", RetrieveUpdateProfile, basename="")


app_name = "prof"
urlpatterns = [
    path("", include(router.urls)),
]
