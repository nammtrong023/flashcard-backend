from django.urls import resolve
from rest_framework.permissions import IsAuthenticated


class CustomPermission(IsAuthenticated):
    EXEMPTED_VIEW_NAMES = [
        'register',
        'login',
        'verify-email',
        'resend-otp',
        'token_refresh',
        'password-reset',
        'reset-password-confirm',
        'set-new-password',
        'update-user',
        'google-oauth',
    ]

    def has_permission(self, request, view):
        match = resolve(request.path)
        view_name = match.url_name

        if view_name in self.EXEMPTED_VIEW_NAMES:
            return True

        return super().has_permission(request, view)
