from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer
)
from drf_yasg.utils import swagger_auto_schema


class GetTokenPairView(generics.GenericAPIView):
    serializer_class = TokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="This endpoint gives a token pair to user"
    )
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

           
class GetAccessTokenView(generics.GenericAPIView):
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(
        operation_description="This endpoint get access token for a valid refresh token"
    )
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class AccessValidatorView(generics.GenericAPIView):
    serializer_class = TokenVerifySerializer

    @swagger_auto_schema(
        operation_description="This endpoint validate access and refresh token"
    )
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)