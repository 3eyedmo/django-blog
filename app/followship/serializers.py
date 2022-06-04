from django.contrib.auth import get_user_model

from rest_framework import serializers




class PeopleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="profile.username")
    image = serializers.CharField(source="profile.image")
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "image"
        )