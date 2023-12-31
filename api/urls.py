from django.urls import include, path

urlpatterns = [
    path("auth/", include('accounts.urls')),
    path("oauth/", include('social_accounts.urls')),
    path("products/", include('product.urls')),
    path("flashcards/", include('flashcards.urls')),
    path("classes/", include('classes.urls')),
]
