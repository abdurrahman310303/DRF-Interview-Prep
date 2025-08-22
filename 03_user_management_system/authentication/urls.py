from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='auth-register'),
    path('login/', UserLoginView.as_view(), name='auth-login'),
    path('logout/', UserLogoutView.as_view(), name='auth-logout'),
    path('change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='auth-password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
]
