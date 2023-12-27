from django.urls import path

from . import views

urlpatterns = [
    path("register", views.RegisterView.as_view()),
    path("verify-email", views.VerifyEmailView.as_view()),
    path("resend-otp", views.ResendOtpView.as_view()),
    path("login", views.LoginView.as_view()),
    path("reset-password", views.PasswordResetRequestView.as_view()),
    path(
        'password-reset/',
        views.PasswordResetRequestView.as_view(),
        name='password-reset',
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        views.PasswordResetConfirm.as_view(),
        name='reset-password-confirm',
    ),
    path(
        'set-new-password/',
        views.SetNewPasswordView.as_view(),
        name='set-new-password',
    ),
]
