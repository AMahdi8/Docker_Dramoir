from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    VerifyEmailView,
    LoginView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    UserProfileView,
    FavoriteListCreateView,
    FavoriteDeleteView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('favorites/', FavoriteListCreateView.as_view(), name='favorite-list-create'),
    path('favorites/<int:content_id>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
] 