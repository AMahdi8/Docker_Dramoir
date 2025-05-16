from django.urls import path
from .views import (
    UserRegistrationView,
    VerifyEmailView,
    LoginView,
    PasswordResetRequestView,
    PasswordResetConfirmView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
] 