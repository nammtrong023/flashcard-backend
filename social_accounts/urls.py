from django.urls import path

from . import views

urlpatterns = [path('login-gg', views.GoogleOauthSignInview.as_view())]
