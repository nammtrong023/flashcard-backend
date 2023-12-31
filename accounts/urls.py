from accounts.utils import public_view
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("register", public_view(views.RegisterView), name='register'),
    path("login", public_view(views.LoginView), name='login'),
    path(
        "verify-email",
        public_view(views.VerifyEmailView),
        name='verify-email',
    ),
    path(
        "resend-otp",
        public_view(views.ResendOtpView),
        name='resend-otp',
    ),
    path(
        'token-refresh/',
        public_view(TokenRefreshView),
        name='token_refresh',
    ),
    path(
        'password-reset/',
        public_view(views.PasswordResetRequestView),
        name='password-reset',
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        public_view(views.PasswordResetConfirm),
        name='reset-password-confirm',
    ),
    path(
        'set-new-password/',
        public_view(views.SetNewPasswordView),
        name='set-new-password',
    ),
    path(
        'users/<int:pk>',
        views.UserRetrieveUpdateDestroyAPIView.as_view(),
        name='users',
    ),
]
