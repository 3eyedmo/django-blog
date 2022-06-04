
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


from accounts.serializers import RegisterSerializer, RegisterTokenVerfication
from accounts.tokens import VerficationPayload
from accounts.utils import send_email


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_description="This endpoint is for registration"
    )
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            user = serializer.create(validated_data=validated_data)
            email = serializer.validated_data.get("email")
            token = VerficationPayload.for_user(user, subject="is_active", value=False)
            send_email(email=email, token=str(token))
            return Response(data={"msg": "email was sent."}, status=200)



class RegisterTokenActivator(generics.GenericAPIView):
    serializer_class = RegisterTokenVerfication
    @swagger_auto_schema(
        operation_description="This schema is for verification of register token."
    )
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(data={"msg": "activated"}, status=status.HTTP_200_OK)

