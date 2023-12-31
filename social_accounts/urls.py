from accounts.utils import public_view
from django.urls import path

from . import views

urlpatterns = [
    path(
        'google-oauth',
        public_view(views.GoogleOauthSignInview),
        name='google-oauth',
    )
]
