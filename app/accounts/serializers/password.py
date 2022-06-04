from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

from rest_framework import serializers

from accounts.exceptions import TokenInvalid




User = get_user_model()


class PasswordForgetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordForgetTokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()
    uidb64 = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        try:
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")
            password1 = attrs.get("password1")
            password2 = attrs.get("password2")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                raise TokenInvalid()

            checked = PasswordResetTokenGenerator().check_token(user=user, token=token)
            
            if password1 != password2:
                raise TokenInvalid()
            
            if len(password2) < 8:
                raise TokenInvalid()

            user.set_password(password2)
            user.save()
            print("This is checked :  ", checked)
            return super().validate(attrs)
            
        except:
            raise TokenInvalid()


class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        print(self.context)
        data["user"] = self.context.get("user")
        return data

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        user = attrs.get("user")

        if password2 != password1:
            raise serializers.ValidationError("passwords dont match")
        if len(password2) < 8:
            raise serializers.ValidationError("password too short")
        if not user.check_password(old_password):
            raise serializers.ValidationError("old password wrong")

        return super().validate(attrs)

    def save(self, **kwargs):
        password2 = self.validated_data.get("password2")
        user = self.validated_data.get("user")
        user.set_password(password2)
        user.save()
        return user
