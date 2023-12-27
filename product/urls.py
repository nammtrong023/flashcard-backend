from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListCreateApiView.as_view()),
    path('sizes', views.SizeListCreateApiView.as_view()),
    path('flashcards', views.FlashcardListCreateApiView.as_view()),
]
