from django.urls import path

from . import views

urlpatterns = [
    path('', views.FlashCardCreateApiView.as_view()),
    path('<int:pk>', views.FlashcardRetrieveUpdateDestroyApiView.as_view()),
    path(
        'flashcard-sets-by-owner/<owner_id>',
        views.FlashcardSetListCreateApiView.as_view(),
    ),
    path(
        'flashcard-sets/<int:pk>',
        views.FlashcardSetRetrieveUpdateDestroyApiView.as_view(),
    ),
    path('viewers', views.FlashcardSetViewerListCreateApiView.as_view()),
    path(
        'viewers-by-fcard-id/<int:pk>',
        views.FlashcardSetViewerByFCardSetIdRetrieveUpdateApiView.as_view(),
    ),
]
