from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from accounts.serializers import (
    PasswordForgetSerializer,
    PasswordForgetTokenVerifySerializer,
    PasswordResetSerializer
)
from accounts.utils import send_email
User = get_user_model()


class PasswordForgetSendEmail(generics.GenericAPIView):
    serializer_class = PasswordForgetSerializer

    @swagger_auto_schema(
        operation_description="This api send to user email a password forget link"
    )
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            current_site = current_site
            relativeLink = f"{token}&uidb64={uidb64}"
            send_email(email=email, token=relativeLink, current_site=current_site, subject="password-reset")
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
                

class PasswordForgetVerify(generics.GenericAPIView):
    serializer_class = PasswordForgetTokenVerifySerializer

    @swagger_auto_schema(
        operation_description="This api validate users token and uidb64 that was sent to email " \
                                    "and creates a new password"
    )
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(
            data= {
                "msg": "password reset successfully!"
            },
            status=status.HTTP_200_OK
        )

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        operation_description=("This api reset user password")
    )
    def post(self, request):
        data = request.data
        context = {
            "user": request.user 
        }
        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data= {
                "msg": "password reset successfully!"
            },
            status=status.HTTP_200_OK
        )