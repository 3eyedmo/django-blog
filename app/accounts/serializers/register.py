from django.contrib.auth import get_user_model

from rest_framework import serializers
import validators

from accounts.tokens import VerficationPayload
from accounts.utils import valid_password
from accounts.exceptions import TokenInvalid

User = get_user_model()

class RegisterTokenVerfication(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get("token", None)
        try:
            token_obj = VerficationPayload(token)
            token_obj.for_registration_verify()
        except:
            raise TokenInvalid()
        return super().validate(attrs)



class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(source="password")
    password2 = serializers.CharField()
    class Meta:
        model=User
        fields = [
            'email',
            'password1',
            'password2'
        ]

    def validate_password2(self, value):
        password1 = self.initial_data.get("password1")
        password2 = value
        valid_password(password1, password2)
        return password2

    def validate_email(self, value):
        email = value
        if not validators.email(email):
            raise serializers.ValidationError("invalid email.")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("email exists.")
        return email


    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password2")
        try:
            user = User.objects.create_user(email=email, password=password)
        except:
            raise serializers.ValidationError("invalid data.")
        return user