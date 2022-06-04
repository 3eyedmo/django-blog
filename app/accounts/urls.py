from django.urls import path

from accounts.views import (
    GetTokenPairView,
    GetAccessTokenView,
    AccessValidatorView,
    RegisterView,
    RegisterTokenActivator,
    PasswordForgetSendEmail,
    PasswordForgetVerify,
    PasswordResetView
)

app_name = 'accounts'

urlpatterns= [
    path('token_pair/', GetTokenPairView.as_view(), name='get_token_pair'),
    path('access/', GetAccessTokenView.as_view(), name='get_access_token'),
    path('access_validate/', AccessValidatorView.as_view(), name='access_validate'),
    path('register/', RegisterView.as_view(), name="register_user"),
    path('register_verify/', RegisterTokenActivator.as_view(), name="email_activator"),
    path('password_forget_email/', PasswordForgetSendEmail.as_view(), name="password_forget_email"),
    path('password_forget_verfication/', PasswordForgetVerify.as_view(), name="password_forget_verfication"),
    path('password_reset/', PasswordResetView.as_view(), name="password_reset")
]